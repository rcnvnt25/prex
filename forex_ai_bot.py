"""
Forex AI Trading Bot with News Sentiment Analysis
Fitur:
- Analisis sentimen berita otomatis menggunakan AI
- Auto open posisi berdasarkan sentiment (bullish/bearish)
- Stop Loss: 1% dari entry price
- Take Profit: 10% dari entry price
- Integrasi dengan MetaTrader 5
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from typing import Dict, List, Tuple
import json


class NewsAnalyzer:
    """Analyzer untuk menganalisis sentimen berita forex"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize News Analyzer
        
        Args:
            api_key: API key untuk news service (opsional)
        """
        self.api_key = api_key
        self.sentiment_keywords = {
            'bullish': [
                'surge', 'rally', 'gain', 'rise', 'increase', 'growth', 'stronger',
                'positive', 'optimistic', 'boost', 'improvement', 'expansion',
                'recovery', 'upbeat', 'soar', 'jump', 'advance'
            ],
            'bearish': [
                'fall', 'drop', 'decline', 'decrease', 'weak', 'loss', 'crash',
                'negative', 'pessimistic', 'concern', 'worry', 'recession',
                'contraction', 'downward', 'plunge', 'tumble', 'slump'
            ]
        }
    
    def analyze_sentiment(self, news_text: str) -> Dict:
        """
        Analisis sentimen dari teks berita
        
        Args:
            news_text: Teks berita yang akan dianalisis
            
        Returns:
            Dict dengan sentiment score dan signal
        """
        news_lower = news_text.lower()
        
        bullish_count = sum(1 for word in self.sentiment_keywords['bullish'] 
                           if word in news_lower)
        bearish_count = sum(1 for word in self.sentiment_keywords['bearish'] 
                           if word in news_lower)
        
        # Hitung sentiment score (-1 to 1)
        total_keywords = bullish_count + bearish_count
        if total_keywords == 0:
            sentiment_score = 0
        else:
            sentiment_score = (bullish_count - bearish_count) / total_keywords
        
        # Tentukan signal
        if sentiment_score > 0.2:
            signal = 'BUY'
            strength = 'strong' if sentiment_score > 0.5 else 'moderate'
        elif sentiment_score < -0.2:
            signal = 'SELL'
            strength = 'strong' if sentiment_score < -0.5 else 'moderate'
        else:
            signal = 'NEUTRAL'
            strength = 'weak'
        
        return {
            'sentiment_score': sentiment_score,
            'signal': signal,
            'strength': strength,
            'bullish_keywords': bullish_count,
            'bearish_keywords': bearish_count,
            'news_text': news_text[:200]  # Preview
        }
    
    def get_forex_news(self, currency_pair: str = 'EURUSD') -> List[Dict]:
        """
        Simulasi mendapatkan berita forex
        Dalam production, gunakan API seperti NewsAPI, Alpha Vantage, dll
        
        Args:
            currency_pair: Pair yang akan dicari beritanya
            
        Returns:
            List of news items
        """
        # Simulasi berita (ganti dengan real API)
        simulated_news = [
            {
                'title': 'EUR Surges on Positive ECB Economic Outlook',
                'content': 'The Euro rallied strongly today as the European Central Bank released an optimistic economic forecast showing growth expansion and improvement in key indicators.',
                'timestamp': datetime.now(),
                'impact': 'high'
            },
            {
                'title': 'USD Weakens Amid Recession Concerns',
                'content': 'The US Dollar tumbled as worrying economic data sparked fears of a potential recession. Negative sentiment continues to weigh on the currency.',
                'timestamp': datetime.now() - timedelta(hours=1),
                'impact': 'high'
            },
            {
                'title': 'GBP Shows Mixed Performance',
                'content': 'The British Pound showed mixed results today with some gains offset by concerns about inflation.',
                'timestamp': datetime.now() - timedelta(hours=2),
                'impact': 'medium'
            }
        ]
        
        return simulated_news


class ForexAIBot:
    """Main trading bot dengan AI news analysis"""
    
    def __init__(self, 
                 symbol: str = 'EURUSD',
                 lot_size: float = 0.01,
                 stop_loss_percent: float = 1.0,
                 take_profit_percent: float = 10.0,
                 magic_number: int = 234000):
        """
        Initialize Forex AI Bot
        
        Args:
            symbol: Trading pair (contoh: 'EURUSD')
            lot_size: Ukuran lot untuk trading
            stop_loss_percent: Stop loss dalam persen (default 1%)
            take_profit_percent: Take profit dalam persen (default 10%)
            magic_number: Magic number untuk identifikasi order
        """
        self.symbol = symbol
        self.lot_size = lot_size
        self.stop_loss_percent = stop_loss_percent / 100
        self.take_profit_percent = take_profit_percent / 100
        self.magic_number = magic_number
        
        self.news_analyzer = NewsAnalyzer()
        self.is_running = False
        
    def connect_mt5(self) -> bool:
        """Connect ke MetaTrader 5"""
        if not mt5.initialize():
            print("❌ MT5 initialization failed")
            print(mt5.last_error())
            return False
        
        print("✅ Connected to MetaTrader 5")
        print(f"MT5 version: {mt5.version()}")
        
        # Check symbol
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info is None:
            print(f"❌ Symbol {self.symbol} not found")
            return False
        
        if not symbol_info.visible:
            if not mt5.symbol_select(self.symbol, True):
                print(f"❌ Failed to select {self.symbol}")
                return False
        
        print(f"✅ Symbol {self.symbol} is ready")
        return True
    
    def calculate_sl_tp(self, order_type: str, entry_price: float) -> Tuple[float, float]:
        """
        Calculate Stop Loss dan Take Profit levels
        
        Args:
            order_type: 'BUY' atau 'SELL'
            entry_price: Harga entry
            
        Returns:
            Tuple of (stop_loss, take_profit)
        """
        if order_type == 'BUY':
            stop_loss = entry_price * (1 - self.stop_loss_percent)
            take_profit = entry_price * (1 + self.take_profit_percent)
        else:  # SELL
            stop_loss = entry_price * (1 + self.stop_loss_percent)
            take_profit = entry_price * (1 - self.take_profit_percent)
        
        return stop_loss, take_profit
    
    def open_position(self, signal: str, sentiment_data: Dict) -> bool:
        """
        Buka posisi trading berdasarkan signal
        
        Args:
            signal: 'BUY' atau 'SELL'
            sentiment_data: Data sentiment dari news analyzer
            
        Returns:
            True jika sukses, False jika gagal
        """
        if signal not in ['BUY', 'SELL']:
            print(f"⚠️  Invalid signal: {signal}")
            return False
        
        # Get current price
        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            print(f"❌ Failed to get tick for {self.symbol}")
            return False
        
        price = tick.ask if signal == 'BUY' else tick.bid
        
        # Calculate SL and TP
        sl, tp = self.calculate_sl_tp(signal, price)
        
        # Prepare request
        point = mt5.symbol_info(self.symbol).point
        deviation = 20
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_BUY if signal == 'BUY' else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": self.magic_number,
            "comment": f"AI_News_{sentiment_data['strength']}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Order failed: {result.comment}")
            return False
        
        print(f"\n{'='*60}")
        print(f"✅ {signal} ORDER OPENED")
        print(f"{'='*60}")
        print(f"Symbol: {self.symbol}")
        print(f"Entry Price: {price:.5f}")
        print(f"Stop Loss: {sl:.5f} (-{self.stop_loss_percent*100}%)")
        print(f"Take Profit: {tp:.5f} (+{self.take_profit_percent*100}%)")
        print(f"Volume: {self.lot_size}")
        print(f"Sentiment Score: {sentiment_data['sentiment_score']:.2f}")
        print(f"Signal Strength: {sentiment_data['strength']}")
        print(f"Order ID: {result.order}")
        print(f"{'='*60}\n")
        
        return True
    
    def check_open_positions(self) -> List:
        """Check posisi yang sedang terbuka"""
        positions = mt5.positions_get(symbol=self.symbol)
        if positions is None:
            return []
        return list(positions)
    
    def monitor_positions(self):
        """Monitor posisi yang sedang berjalan"""
        positions = self.check_open_positions()
        
        if len(positions) == 0:
            return
        
        print(f"\n📊 Monitoring {len(positions)} open position(s)...")
        
        for pos in positions:
            # Calculate current profit percentage
            if pos.type == mt5.ORDER_TYPE_BUY:
                profit_pct = ((pos.price_current - pos.price_open) / pos.price_open) * 100
            else:
                profit_pct = ((pos.price_open - pos.price_current) / pos.price_open) * 100
            
            print(f"Position #{pos.ticket}: {profit_pct:+.2f}% | "
                  f"P/L: ${pos.profit:.2f} | "
                  f"Price: {pos.price_current:.5f}")
    
    def process_news_and_trade(self):
        """Process berita dan execute trading berdasarkan sentiment"""
        print("\n🔍 Fetching latest forex news...")
        
        # Get news
        news_items = self.news_analyzer.get_forex_news(self.symbol)
        
        for news in news_items:
            print(f"\n📰 News: {news['title']}")
            
            # Analyze sentiment
            sentiment = self.news_analyzer.analyze_sentiment(
                news['title'] + ' ' + news['content']
            )
            
            print(f"   Sentiment: {sentiment['signal']} "
                  f"(Score: {sentiment['sentiment_score']:.2f}, "
                  f"Strength: {sentiment['strength']})")
            
            # Check if already have open position
            positions = self.check_open_positions()
            if len(positions) > 0:
                print(f"   ⚠️  Already have {len(positions)} open position(s). Skipping...")
                continue
            
            # Open position jika signal strong atau moderate
            if sentiment['signal'] in ['BUY', 'SELL'] and sentiment['strength'] in ['strong', 'moderate']:
                print(f"   🎯 Trading signal detected: {sentiment['signal']}")
                self.open_position(sentiment['signal'], sentiment)
                break  # Process satu news saja per cycle
    
    def run(self, check_interval: int = 60):
        """
        Jalankan bot secara continuous
        
        Args:
            check_interval: Interval pengecekan dalam detik (default 60)
        """
        if not self.connect_mt5():
            return
        
        self.is_running = True
        print(f"\n{'='*60}")
        print(f"🤖 FOREX AI BOT STARTED")
        print(f"{'='*60}")
        print(f"Symbol: {self.symbol}")
        print(f"Lot Size: {self.lot_size}")
        print(f"Stop Loss: {self.stop_loss_percent*100}%")
        print(f"Take Profit: {self.take_profit_percent*100}%")
        print(f"Check Interval: {check_interval}s")
        print(f"{'='*60}\n")
        
        try:
            while self.is_running:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Monitor existing positions
                self.monitor_positions()
                
                # Process news and potentially open new positions
                self.process_news_and_trade()
                
                # Wait for next cycle
                print(f"\n💤 Waiting {check_interval} seconds for next check...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Bot stopped by user")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown bot dan close MT5 connection"""
        self.is_running = False
        mt5.shutdown()
        print("\n✅ Bot shutdown complete")


def main():
    """Main function untuk menjalankan bot"""
    
    # Konfigurasi bot
    config = {
        'symbol': 'EURUSD',           # Pair yang akan ditrade
        'lot_size': 0.01,             # Ukuran lot (0.01 = 1 micro lot)
        'stop_loss_percent': 1.0,     # Stop loss 1%
        'take_profit_percent': 10.0,  # Take profit 10%
        'check_interval': 60          # Check setiap 60 detik
    }
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         FOREX AI BOT - NEWS SENTIMENT TRADING             ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Fitur:
    ✓ Analisis sentimen berita otomatis
    ✓ Auto open posisi berdasarkan good/bad news
    ✓ Stop Loss otomatis: 1% dari entry
    ✓ Take Profit otomatis: 10% dari entry
    ✓ Integrasi penuh dengan MT5
    
    """)
    
    # Create dan jalankan bot
    bot = ForexAIBot(
        symbol=config['symbol'],
        lot_size=config['lot_size'],
        stop_loss_percent=config['stop_loss_percent'],
        take_profit_percent=config['take_profit_percent']
    )
    
    # Run bot
    bot.run(check_interval=config['check_interval'])


if __name__ == "__main__":
    main()
