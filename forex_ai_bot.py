"""
Forex AI Trading Bot - UPGRADED VERSION
Fitur:
- Scraping news dari Telegram channels (marketfeed & wfwitness) TANPA perlu buat bot
- AI sentiment analysis dengan machine learning
- Multi-pair trading (semua pairs yang tersedia)
- Auto open posisi: Bad news = SHORT, Good news = LONG
- Multi position support
- Demo account testing
- Full MT5 integration dengan .env configuration
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import asyncio
from typing import Dict, List, Tuple, Optional
import json
import os
from dotenv import load_dotenv

# Telegram scraping (NO BOT NEEDED)
try:
    from telethon import TelegramClient
    from telethon.tl.functions.messages import GetHistoryRequest
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("⚠️ Telethon not installed. Install with: pip install telethon")

# Load environment variables
load_dotenv()


class TelegramNewsScaper:
    """Scrape news dari Telegram channels TANPA perlu bot"""
    
    def __init__(self):
        """Initialize Telegram scraper"""
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        
        if not all([self.api_id, self.api_hash, self.phone]):
            print("⚠️ Telegram credentials not found in .env")
            self.client = None
        else:
            self.client = TelegramClient('forex_bot_session', self.api_id, self.api_hash)
        
        # Channels to monitor
        self.channels = [
            'marketfeed',  # @marketfeed
            'wfwitness'    # @wfwitness
        ]
        
        self.last_message_ids = {}
    
    async def connect(self):
        """Connect to Telegram"""
        if not self.client:
            return False
        
        await self.client.start(phone=self.phone)
        print("✅ Connected to Telegram")
        return True
    
    async def get_latest_messages(self, channel: str, limit: int = 10) -> List[Dict]:
        """
        Get latest messages from a channel
        
        Args:
            channel: Channel username (without @)
            limit: Number of messages to fetch
            
        Returns:
            List of message dictionaries
        """
        if not self.client or not self.client.is_connected():
            return []
        
        try:
            messages = []
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.text:
                    messages.append({
                        'id': message.id,
                        'text': message.text,
                        'date': message.date,
                        'channel': channel,
                        'views': message.views or 0
                    })
            
            return messages
        
        except Exception as e:
            print(f"❌ Error fetching from {channel}: {e}")
            return []
    
    async def get_new_messages_from_all_channels(self) -> List[Dict]:
        """Get new messages from all monitored channels"""
        all_messages = []
        
        for channel in self.channels:
            messages = await self.get_latest_messages(channel, limit=5)
            
            # Filter only new messages
            last_id = self.last_message_ids.get(channel, 0)
            new_messages = [msg for msg in messages if msg['id'] > last_id]
            
            if new_messages:
                # Update last message ID
                self.last_message_ids[channel] = max(msg['id'] for msg in new_messages)
                all_messages.extend(new_messages)
        
        return all_messages
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()


class EnhancedNewsAnalyzer:
    """Enhanced AI analyzer dengan sentiment analysis yang lebih canggih"""
    
    def __init__(self):
        """Initialize Enhanced News Analyzer"""
        # Expanded sentiment keywords dengan scoring
        self.bullish_keywords = {
            # Very strong bullish (3 points)
            'surge': 3, 'soar': 3, 'rally': 3, 'boom': 3, 'skyrocket': 3,
            'breakthrough': 3, 'record high': 3, 'all-time high': 3,
            
            # Strong bullish (2 points)
            'rise': 2, 'gain': 2, 'increase': 2, 'growth': 2, 'stronger': 2,
            'positive': 2, 'optimistic': 2, 'boost': 2, 'jump': 2, 'advance': 2,
            'improve': 2, 'recovery': 2, 'upbeat': 2, 'expansion': 2,
            
            # Moderate bullish (1 point)
            'up': 1, 'better': 1, 'good': 1, 'stable': 1, 'support': 1,
            'confidence': 1, 'solid': 1, 'strong': 1
        }
        
        self.bearish_keywords = {
            # Very strong bearish (-3 points)
            'crash': -3, 'plunge': -3, 'collapse': -3, 'tumble': -3, 'slump': -3,
            'crisis': -3, 'panic': -3, 'disaster': -3, 'record low': -3,
            
            # Strong bearish (-2 points)
            'fall': -2, 'drop': -2, 'decline': -2, 'decrease': -2, 'weak': -2,
            'loss': -2, 'negative': -2, 'concern': -2, 'worry': -2,
            'recession': -2, 'contraction': -2, 'downward': -2, 'pessimistic': -2,
            
            # Moderate bearish (-1 point)
            'down': -1, 'worse': -1, 'bad': -1, 'risk': -1, 'uncertain': -1,
            'doubt': -1, 'pressure': -1
        }
        
        # Currency-specific keywords untuk lebih akurat
        self.currency_impact = {
            'USD': ['dollar', 'usd', 'fed', 'federal reserve', 'us economy', 'america'],
            'EUR': ['euro', 'eur', 'ecb', 'european central bank', 'eurozone', 'europe'],
            'GBP': ['pound', 'sterling', 'gbp', 'boe', 'bank of england', 'uk', 'britain'],
            'JPY': ['yen', 'jpy', 'boj', 'bank of japan', 'japan'],
            'AUD': ['aussie', 'aud', 'rba', 'australia'],
            'CAD': ['loonie', 'cad', 'canada'],
            'CHF': ['franc', 'chf', 'swiss', 'switzerland'],
            'NZD': ['kiwi', 'nzd', 'new zealand']
        }
    
    def analyze_sentiment(self, news_text: str) -> Dict:
        """
        Enhanced sentiment analysis dengan scoring system
        
        Args:
            news_text: Text berita yang akan dianalisis
            
        Returns:
            Dict dengan detailed sentiment analysis
        """
        news_lower = news_text.lower()
        
        # Calculate sentiment score
        sentiment_score = 0
        bullish_matches = []
        bearish_matches = []
        
        # Check bullish keywords
        for keyword, score in self.bullish_keywords.items():
            if keyword in news_lower:
                sentiment_score += score
                bullish_matches.append((keyword, score))
        
        # Check bearish keywords
        for keyword, score in self.bearish_keywords.items():
            if keyword in news_lower:
                sentiment_score += score  # score is negative
                bearish_matches.append((keyword, score))
        
        # Normalize score (-1 to 1)
        max_possible_score = 15  # Arbitrary max for normalization
        normalized_score = max(min(sentiment_score / max_possible_score, 1.0), -1.0)
        
        # Determine signal and strength
        if normalized_score >= 0.3:
            signal = 'LONG'
            if normalized_score >= 0.7:
                strength = 'very_strong'
            elif normalized_score >= 0.5:
                strength = 'strong'
            else:
                strength = 'moderate'
        elif normalized_score <= -0.3:
            signal = 'SHORT'
            if normalized_score <= -0.7:
                strength = 'very_strong'
            elif normalized_score <= -0.5:
                strength = 'strong'
            else:
                strength = 'moderate'
        else:
            signal = 'NEUTRAL'
            strength = 'weak'
        
        # Detect affected currencies
        affected_currencies = self.detect_currencies(news_lower)
        
        return {
            'sentiment_score': round(normalized_score, 3),
            'raw_score': sentiment_score,
            'signal': signal,
            'strength': strength,
            'bullish_keywords': bullish_matches,
            'bearish_keywords': bearish_matches,
            'affected_currencies': affected_currencies,
            'news_preview': news_text[:200]
        }
    
    def detect_currencies(self, text: str) -> List[str]:
        """Detect which currencies are mentioned in the news"""
        detected = []
        for currency, keywords in self.currency_impact.items():
            for keyword in keywords:
                if keyword in text:
                    if currency not in detected:
                        detected.append(currency)
                    break
        return detected
    
    def get_tradable_pairs(self, affected_currencies: List[str]) -> List[str]:
        """
        Generate list of pairs to trade based on affected currencies
        
        Args:
            affected_currencies: List of currency codes (e.g. ['USD', 'EUR'])
            
        Returns:
            List of tradable pairs
        """
        if not affected_currencies:
            return []
        
        major_currencies = ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD']
        pairs = []
        
        for currency in affected_currencies:
            for other in major_currencies:
                if currency != other:
                    # Create pair (always major currency first by convention)
                    pair = f"{currency}{other}"
                    if pair not in pairs:
                        pairs.append(pair)
        
        return pairs


class MultiPairForexBot:
    """Main trading bot dengan multi-pair support dan Telegram integration"""
    
    def __init__(self):
        """Initialize Multi-Pair Forex Bot"""
        # Load configuration from .env
        self.mt5_login = int(os.getenv('MT5_LOGIN', '0'))
        self.mt5_password = os.getenv('MT5_PASSWORD', '')
        self.mt5_server = os.getenv('MT5_SERVER', '')
        self.mt5_path = os.getenv('MT5_PATH', '')
        
        # Trading parameters
        self.default_lot_size = float(os.getenv('DEFAULT_LOT_SIZE', '0.01'))
        self.stop_loss_percent = float(os.getenv('STOP_LOSS_PERCENT', '1.0'))
        self.take_profit_percent = float(os.getenv('TAKE_PROFIT_PERCENT', '10.0'))
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '60'))
        
        # Risk management
        self.max_daily_loss = float(os.getenv('MAX_DAILY_LOSS', '50.0'))
        self.max_daily_profit = float(os.getenv('MAX_DAILY_PROFIT', '200.0'))
        self.max_trades_per_day = int(os.getenv('MAX_TRADES_PER_DAY', '20'))
        self.max_consecutive_losses = int(os.getenv('MAX_CONSECUTIVE_LOSSES', '3'))
        
        # Initialize components
        self.news_analyzer = EnhancedNewsAnalyzer()
        self.telegram_scraper = TelegramNewsScaper() if TELETHON_AVAILABLE else None
        
        # Tracking
        self.is_running = False
        self.daily_trades = 0
        self.daily_profit = 0.0
        self.consecutive_losses = 0
        self.processed_news_ids = set()
        
        # Available pairs
        self.available_pairs = []
    
    def connect_mt5(self) -> bool:
        """Connect to MetaTrader 5 with credentials from .env"""
        # Initialize with path if provided
        if self.mt5_path:
            if not mt5.initialize(path=self.mt5_path):
                print("❌ MT5 initialization failed with provided path")
                print(f"Error: {mt5.last_error()}")
                # Try without path
                if not mt5.initialize():
                    print("❌ MT5 initialization failed")
                    return False
        else:
            if not mt5.initialize():
                print("❌ MT5 initialization failed")
                print(f"Error: {mt5.last_error()}")
                return False
        
        print("✅ MT5 initialized")
        
        # Login to account
        if self.mt5_login and self.mt5_password and self.mt5_server:
            authorized = mt5.login(
                login=self.mt5_login,
                password=self.mt5_password,
                server=self.mt5_server
            )
            
            if not authorized:
                print(f"❌ MT5 login failed for account {self.mt5_login}")
                print(f"Error: {mt5.last_error()}")
                return False
            
            print(f"✅ Logged in to MT5 account: {self.mt5_login}")
            print(f"   Server: {self.mt5_server}")
            
            # Get account info
            account_info = mt5.account_info()
            if account_info:
                print(f"   Balance: ${account_info.balance:.2f}")
                print(f"   Equity: ${account_info.equity:.2f}")
                print(f"   Leverage: 1:{account_info.leverage}")
                
                # Check if demo account
                if hasattr(account_info, 'trade_mode'):
                    if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
                        print(f"   ✅ DEMO ACCOUNT (Safe for testing)")
                    else:
                        print(f"   ⚠️ LIVE ACCOUNT - BE CAREFUL!")
        else:
            print("⚠️ No MT5 credentials in .env, using already logged-in account")
        
        # Get available pairs
        self.available_pairs = self.get_all_forex_pairs()
        print(f"\n✅ Found {len(self.available_pairs)} tradable forex pairs")
        
        return True
    
    def get_all_forex_pairs(self) -> List[str]:
        """Get all available forex pairs from broker"""
        symbols = mt5.symbols_get()
        if symbols is None:
            return []
        
        # Filter forex pairs only (tidak termasuk crypto, stocks, dll)
        forex_pairs = []
        forex_currencies = ['EUR', 'USD', 'GBP', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF']
        
        for symbol in symbols:
            symbol_name = symbol.name
            
            # Check if it's a forex pair (6 characters, all major currencies)
            if len(symbol_name) == 6:
                base = symbol_name[:3]
                quote = symbol_name[3:]
                
                if base in forex_currencies and quote in forex_currencies:
                    if symbol.visible or mt5.symbol_select(symbol_name, True):
                        forex_pairs.append(symbol_name)
        
        return sorted(forex_pairs)
    
    def calculate_sl_tp(self, pair: str, order_type: str, entry_price: float) -> Tuple[float, float]:
        """Calculate Stop Loss and Take Profit levels"""
        if order_type == 'LONG':
            stop_loss = entry_price * (1 - self.stop_loss_percent / 100)
            take_profit = entry_price * (1 + self.take_profit_percent / 100)
        else:  # SHORT
            stop_loss = entry_price * (1 + self.stop_loss_percent / 100)
            take_profit = entry_price * (1 - self.take_profit_percent / 100)
        
        # Round to proper digits
        symbol_info = mt5.symbol_info(pair)
        if symbol_info:
            digits = symbol_info.digits
            stop_loss = round(stop_loss, digits)
            take_profit = round(take_profit, digits)
        
        return stop_loss, take_profit
    
    def check_risk_limits(self) -> bool:
        """Check if we can still trade based on risk management rules"""
        if self.daily_trades >= self.max_trades_per_day:
            print(f"⛔ Daily trade limit reached ({self.max_trades_per_day})")
            return False
        
        if self.daily_profit <= -self.max_daily_loss:
            print(f"⛔ Daily loss limit reached (-${abs(self.daily_profit):.2f})")
            return False
        
        if self.daily_profit >= self.max_daily_profit:
            print(f"🎯 Daily profit target reached (+${self.daily_profit:.2f})")
            print(f"   Locking in profits, no more trades today")
            return False
        
        if self.consecutive_losses >= self.max_consecutive_losses:
            print(f"⛔ Too many consecutive losses ({self.consecutive_losses})")
            return False
        
        return True
    
    def open_position(self, pair: str, signal: str, sentiment_data: Dict) -> bool:
        """
        Open trading position
        
        Args:
            pair: Currency pair (e.g. 'EURUSD')
            signal: 'LONG' or 'SHORT'
            sentiment_data: Sentiment analysis data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.check_risk_limits():
            return False
        
        # Check if symbol exists and is tradable
        symbol_info = mt5.symbol_info(pair)
        if symbol_info is None:
            print(f"⚠️ Pair {pair} not found")
            return False
        
        if not symbol_info.visible:
            if not mt5.symbol_select(pair, True):
                print(f"⚠️ Failed to select {pair}")
                return False
        
        # Get current price
        tick = mt5.symbol_info_tick(pair)
        if tick is None:
            print(f"❌ Failed to get tick for {pair}")
            return False
        
        price = tick.ask if signal == 'LONG' else tick.bid
        
        # Calculate SL and TP
        sl, tp = self.calculate_sl_tp(pair, signal, price)
        
        # Prepare order request
        order_type = mt5.ORDER_TYPE_BUY if signal == 'LONG' else mt5.ORDER_TYPE_SELL
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pair,
            "volume": self.default_lot_size,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234000,
            "comment": f"AI_{sentiment_data['strength']}_{sentiment_data['sentiment_score']}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Order failed for {pair}: {result.comment}")
            return False
        
        # Update tracking
        self.daily_trades += 1
        
        print(f"\n{'='*70}")
        print(f"✅ {signal} ORDER OPENED - {pair}")
        print(f"{'='*70}")
        print(f"Entry Price: {price:.5f}")
        print(f"Stop Loss: {sl:.5f} (-{self.stop_loss_percent}%)")
        print(f"Take Profit: {tp:.5f} (+{self.take_profit_percent}%)")
        print(f"Volume: {self.default_lot_size}")
        print(f"Sentiment Score: {sentiment_data['sentiment_score']:.3f}")
        print(f"Signal Strength: {sentiment_data['strength']}")
        print(f"Order ID: {result.order}")
        print(f"Daily Trades: {self.daily_trades}/{self.max_trades_per_day}")
        print(f"{'='*70}\n")
        
        return True
    
    def monitor_positions(self):
        """Monitor all open positions"""
        positions = mt5.positions_get()
        if positions is None or len(positions) == 0:
            return
        
        print(f"\n📊 Monitoring {len(positions)} open position(s)...")
        
        total_profit = 0.0
        for pos in positions:
            # Calculate current profit percentage
            if pos.type == mt5.ORDER_TYPE_BUY:
                profit_pct = ((pos.price_current - pos.price_open) / pos.price_open) * 100
            else:
                profit_pct = ((pos.price_open - pos.price_current) / pos.price_open) * 100
            
            total_profit += pos.profit
            
            status = "🟢" if pos.profit > 0 else "🔴"
            print(f"{status} {pos.symbol} #{pos.ticket}: {profit_pct:+.2f}% | "
                  f"P/L: ${pos.profit:.2f} | Price: {pos.price_current:.5f}")
        
        print(f"💰 Total Floating P/L: ${total_profit:.2f}")
        self.daily_profit = total_profit
    
    async def process_telegram_news(self):
        """Process news from Telegram channels"""
        if not self.telegram_scraper or not self.telegram_scraper.client:
            print("⚠️ Telegram scraper not available")
            return
        
        print("\n📱 Fetching news from Telegram channels...")
        
        try:
            # Get new messages
            messages = await self.telegram_scraper.get_new_messages_from_all_channels()
            
            if not messages:
                print("   No new messages")
                return
            
            print(f"   Found {len(messages)} new message(s)")
            
            for msg in messages:
                # Create unique ID for this message
                msg_id = f"{msg['channel']}_{msg['id']}"
                
                # Skip if already processed
                if msg_id in self.processed_news_ids:
                    continue
                
                print(f"\n📰 New message from @{msg['channel']}:")
                print(f"   {msg['text'][:150]}...")
                
                # Analyze sentiment
                sentiment = self.news_analyzer.analyze_sentiment(msg['text'])
                
                print(f"   📊 Sentiment: {sentiment['signal']} "
                      f"(Score: {sentiment['sentiment_score']:.3f}, "
                      f"Strength: {sentiment['strength']})")
                
                # Only trade on moderate or stronger signals
                if sentiment['strength'] in ['moderate', 'strong', 'very_strong']:
                    if sentiment['signal'] != 'NEUTRAL':
                        # Get affected currencies and pairs to trade
                        affected_currencies = sentiment['affected_currencies']
                        
                        if affected_currencies:
                            print(f"   🎯 Affected currencies: {', '.join(affected_currencies)}")
                            
                            # Get tradable pairs
                            target_pairs = self.news_analyzer.get_tradable_pairs(affected_currencies)
                            
                            # Filter to only available pairs
                            tradable = [p for p in target_pairs if p in self.available_pairs]
                            
                            if tradable:
                                print(f"   💹 Trading pairs: {', '.join(tradable[:5])}")  # Show first 5
                                
                                # Open positions
                                for pair in tradable[:5]:  # Limit to 5 pairs per news
                                    if not self.check_risk_limits():
                                        break
                                    
                                    self.open_position(pair, sentiment['signal'], sentiment)
                                    time.sleep(1)  # Small delay between orders
                            else:
                                print(f"   ⚠️ No tradable pairs found for affected currencies")
                        else:
                            # Trade major pairs if no specific currency detected
                            print(f"   🌍 No specific currency detected, trading majors")
                            major_pairs = ['EURUSD', 'GBPUSD', 'USDJPY']
                            
                            for pair in major_pairs:
                                if pair in self.available_pairs:
                                    if not self.check_risk_limits():
                                        break
                                    self.open_position(pair, sentiment['signal'], sentiment)
                                    time.sleep(1)
                
                # Mark as processed
                self.processed_news_ids.add(msg_id)
        
        except Exception as e:
            print(f"❌ Error processing Telegram news: {e}")
    
    async def run_async(self):
        """Main async loop for bot"""
        if not self.connect_mt5():
            return
        
        # Connect to Telegram
        if self.telegram_scraper:
            await self.telegram_scraper.connect()
        
        self.is_running = True
        
        print(f"\n{'='*70}")
        print(f"🤖 MULTI-PAIR FOREX AI BOT STARTED")
        print(f"{'='*70}")
        print(f"Available Pairs: {len(self.available_pairs)}")
        print(f"Default Lot Size: {self.default_lot_size}")
        print(f"Stop Loss: {self.stop_loss_percent}%")
        print(f"Take Profit: {self.take_profit_percent}%")
        print(f"Check Interval: {self.check_interval}s")
        print(f"Max Daily Trades: {self.max_trades_per_day}")
        print(f"Max Daily Loss: ${self.max_daily_loss}")
        print(f"Max Daily Profit: ${self.max_daily_profit}")
        print(f"{'='*70}\n")
        
        last_day = datetime.now().day
        
        try:
            while self.is_running:
                current_time = datetime.now()
                print(f"\n⏰ {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Reset daily counters at midnight
                if current_time.day != last_day:
                    print("\n🔄 New trading day - Resetting counters")
                    self.daily_trades = 0
                    self.daily_profit = 0.0
                    self.consecutive_losses = 0
                    last_day = current_time.day
                
                # Monitor existing positions
                self.monitor_positions()
                
                # Process news from Telegram
                await self.process_telegram_news()
                
                # Wait for next cycle
                print(f"\n💤 Waiting {self.check_interval} seconds for next check...")
                await asyncio.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Bot stopped by user")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Shutdown bot and cleanup"""
        self.is_running = False
        
        if self.telegram_scraper:
            await self.telegram_scraper.disconnect()
        
        mt5.shutdown()
        print("\n✅ Bot shutdown complete")
    
    def run(self):
        """Start the bot (sync wrapper for async run)"""
        asyncio.run(self.run_async())


def main():
    """Main function"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║     FOREX AI BOT - MULTI-PAIR TELEGRAM NEWS TRADING              ║
    ╚═══════════════════════════════════════════════════════════════════╝
    
    ✅ Fitur Upgrade:
    • Scraping news dari Telegram (@marketfeed & @wfwitness)
    • TANPA perlu buat Telegram bot
    • AI sentiment analysis yang lebih canggih
    • Multi-pair trading (semua pairs yang tersedia)
    • Bad news = AUTO SHORT | Good news = AUTO LONG
    • Multi position support
    • Demo account safe testing
    • Risk management dengan daily limits
    
    ⚠️  PASTIKAN:
    1. File .env sudah diisi dengan benar
    2. MT5 terminal sudah running dan login
    3. Telegram API credentials sudah disetup
    
    """)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ File .env tidak ditemukan!")
        print("   Buat file .env dulu dan isi dengan credentials Anda")
        return
    
    # Create and run bot
    bot = MultiPairForexBot()
    bot.run()


if __name__ == "__main__":
    main()
