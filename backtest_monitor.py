"""
Backtesting & Monitoring Tools - UPGRADED VERSION
Tools untuk test performance bot dan monitor multi-pair trading
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os


class TradingMonitor:
    """Enhanced monitor untuk track multi-pair trading performance"""
    
    def __init__(self, log_file: str = 'trading_log.json'):
        """
        Initialize Trading Monitor
        
        Args:
            log_file: File untuk menyimpan trading log
        """
        self.log_file = log_file
        self.trades_history = []
        self.load_history()
    
    def load_history(self):
        """Load trading history dari file"""
        try:
            with open(self.log_file, 'r') as f:
                self.trades_history = json.load(f)
            print(f"✅ Loaded {len(self.trades_history)} trades from history")
        except FileNotFoundError:
            self.trades_history = []
            print("📝 Starting fresh trading log")
    
    def save_history(self):
        """Save trading history ke file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.trades_history, f, indent=2, default=str)
    
    def log_trade(self, trade_data: Dict):
        """
        Log trade baru
        
        Args:
            trade_data: Dictionary berisi info trade
        """
        trade_data['timestamp'] = datetime.now().isoformat()
        self.trades_history.append(trade_data)
        self.save_history()
    
    def get_performance_stats(self, pair: Optional[str] = None) -> Dict:
        """
        Calculate performance statistics
        
        Args:
            pair: Filter by specific pair (None = all pairs)
        
        Returns:
            Dictionary berisi statistik trading
        """
        if not self.trades_history:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'total_profit': 0,
            }
        
        # Filter by pair if specified
        if pair:
            trades = [t for t in self.trades_history if t.get('symbol') == pair]
        else:
            trades = self.trades_history
        
        if not trades:
            return {'total_trades': 0}
        
        df = pd.DataFrame(trades)
        
        total_trades = len(df)
        winning_trades = len(df[df['profit'] > 0])
        losing_trades = len(df[df['profit'] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_profit = df['profit'].sum()
        total_wins = df[df['profit'] > 0]['profit'].sum()
        total_losses = abs(df[df['profit'] < 0]['profit'].sum())
        
        profit_factor = (total_wins / total_losses) if total_losses > 0 else 0
        
        avg_win = df[df['profit'] > 0]['profit'].mean() if winning_trades > 0 else 0
        avg_loss = df[df['profit'] < 0]['profit'].mean() if losing_trades > 0 else 0
        
        # Calculate expectancy
        expectancy = (win_rate/100 * avg_win) + ((1-win_rate/100) * avg_loss)
        
        return {
            'pair': pair if pair else 'ALL',
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'total_profit': round(total_profit, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'expectancy': round(expectancy, 2),
            'largest_win': round(df['profit'].max(), 2) if total_trades > 0 else 0,
            'largest_loss': round(df['profit'].min(), 2) if total_trades > 0 else 0,
            'avg_trade_duration': self._calculate_avg_duration(df) if total_trades > 0 else "N/A"
        }
    
    def _calculate_avg_duration(self, df: pd.DataFrame) -> str:
        """Calculate average trade duration"""
        if 'open_time' not in df.columns or 'close_time' not in df.columns:
            return "N/A"
        
        try:
            df['open_time'] = pd.to_datetime(df['open_time'])
            df['close_time'] = pd.to_datetime(df['close_time'])
            df['duration'] = df['close_time'] - df['open_time']
            avg_duration = df['duration'].mean()
            
            # Convert to hours
            hours = avg_duration.total_seconds() / 3600
            return f"{hours:.1f}h"
        except:
            return "N/A"
    
    def print_performance_report(self, by_pair: bool = False):
        """
        Print detailed performance report
        
        Args:
            by_pair: Show breakdown by pair
        """
        # Overall stats
        stats = self.get_performance_stats()
        
        print("\n" + "="*70)
        print("📊 TRADING PERFORMANCE REPORT")
        print("="*70)
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Winning Trades: {stats['winning_trades']} ({stats['win_rate']}%)")
        print(f"Losing Trades: {stats['losing_trades']}")
        print(f"Profit Factor: {stats['profit_factor']}")
        print(f"Expectancy: ${stats['expectancy']} per trade")
        print(f"-"*70)
        print(f"Total P/L: ${stats['total_profit']}")
        print(f"Average Win: ${stats['avg_win']}")
        print(f"Average Loss: ${stats['avg_loss']}")
        print(f"Largest Win: ${stats['largest_win']}")
        print(f"Largest Loss: ${stats['largest_loss']}")
        print(f"Avg Trade Duration: {stats['avg_trade_duration']}")
        print("="*70)
        
        # Performance grade
        if stats['profit_factor'] >= 2.0 and stats['win_rate'] >= 60:
            print("🏆 EXCELLENT PERFORMANCE")
        elif stats['profit_factor'] >= 1.5 and stats['win_rate'] >= 50:
            print("👍 GOOD PERFORMANCE")
        elif stats['profit_factor'] >= 1.0:
            print("✅ PROFITABLE")
        else:
            print("⚠️ NEEDS IMPROVEMENT")
        print("="*70 + "\n")
        
        # By-pair breakdown
        if by_pair and self.trades_history:
            print("\n📈 PERFORMANCE BY PAIR")
            print("="*70)
            
            # Get unique pairs
            df = pd.DataFrame(self.trades_history)
            if 'symbol' in df.columns:
                pairs = df['symbol'].unique()
                
                # Get stats for each pair
                pair_stats = []
                for pair in pairs:
                    pair_stat = self.get_performance_stats(pair)
                    if pair_stat['total_trades'] > 0:
                        pair_stats.append(pair_stat)
                
                # Sort by total profit
                pair_stats.sort(key=lambda x: x['total_profit'], reverse=True)
                
                # Print table header
                print(f"{'Pair':<10} {'Trades':<8} {'Win%':<8} {'P/L':<12} {'PF':<8}")
                print("-"*70)
                
                for ps in pair_stats:
                    print(f"{ps['pair']:<10} {ps['total_trades']:<8} "
                          f"{ps['win_rate']:<8.1f} ${ps['total_profit']:<11.2f} "
                          f"{ps['profit_factor']:<8.2f}")
                
                print("="*70 + "\n")
    
    def get_daily_summary(self, date: datetime = None) -> Dict:
        """
        Get trading summary untuk hari tertentu
        
        Args:
            date: Tanggal yang akan dicek (default: today)
            
        Returns:
            Dictionary berisi summary harian
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y-%m-%d')
        
        daily_trades = [
            t for t in self.trades_history 
            if t.get('timestamp', '').startswith(date_str)
        ]
        
        if not daily_trades:
            return {
                'date': date_str,
                'trades': 0,
                'profit': 0,
            }
        
        df = pd.DataFrame(daily_trades)
        
        return {
            'date': date_str,
            'trades': len(df),
            'wins': len(df[df['profit'] > 0]),
            'losses': len(df[df['profit'] < 0]),
            'profit': round(df['profit'].sum(), 2),
            'win_rate': round((len(df[df['profit'] > 0]) / len(df)) * 100, 1)
        }
    
    def get_weekly_summary(self) -> List[Dict]:
        """Get summary untuk 7 hari terakhir"""
        summaries = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            summary = self.get_daily_summary(date)
            summaries.append(summary)
        return summaries
    
    def export_to_csv(self, filename: str = 'trades_export.csv'):
        """Export trades ke CSV untuk analysis"""
        if not self.trades_history:
            print("⚠️ No trades to export")
            return
        
        df = pd.DataFrame(self.trades_history)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(df)} trades to {filename}")


class EnhancedBacktestEngine:
    """Enhanced backtest engine dengan multi-pair support"""
    
    def __init__(self, initial_balance: float = 10000):
        """
        Initialize Enhanced Backtest Engine
        
        Args:
            initial_balance: Modal awal untuk backtest
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity = initial_balance
        self.trades = []
        self.open_positions = {}
    
    def simulate_multi_pair_trade(self,
                                  pairs: List[str],
                                  signal: str,
                                  lot_size: float,
                                  sl_percent: float,
                                  tp_percent: float,
                                  sentiment_score: float = 0.5) -> List[Dict]:
        """
        Simulate trading multiple pairs simultaneously
        
        Args:
            pairs: List of currency pairs
            signal: 'LONG' or 'SHORT'
            lot_size: Lot size per pair
            sl_percent: Stop loss percent
            tp_percent: Take profit percent
            sentiment_score: Sentiment strength (affects win probability)
        
        Returns:
            List of trade results
        """
        results = []
        
        for pair in pairs:
            # Base price (simulated)
            base_prices = {
                'EURUSD': 1.0850, 'GBPUSD': 1.2650, 'USDJPY': 110.50,
                'AUDUSD': 0.7350, 'USDCAD': 1.2550, 'NZDUSD': 0.6850,
                'USDCHF': 0.9250, 'EURGBP': 0.8580, 'EURJPY': 119.90,
                'GBPJPY': 139.80
            }
            
            entry_price = base_prices.get(pair, 1.0) + np.random.uniform(-0.01, 0.01)
            
            # Win probability based on sentiment
            base_win_prob = 0.5
            sentiment_bonus = abs(sentiment_score) * 0.3  # Max +30% win prob
            win_prob = min(base_win_prob + sentiment_bonus, 0.85)  # Cap at 85%
            
            # Simulate outcome
            outcome = np.random.choice(['tp', 'sl'], p=[win_prob, 1-win_prob])
            
            if signal == 'LONG':
                sl_price = entry_price * (1 - sl_percent / 100)
                tp_price = entry_price * (1 + tp_percent / 100)
                profit_pct = tp_percent if outcome == 'tp' else -sl_percent
            else:  # SHORT
                sl_price = entry_price * (1 + sl_percent / 100)
                tp_price = entry_price * (1 - tp_percent / 100)
                profit_pct = tp_percent if outcome == 'tp' else -sl_percent
            
            profit_usd = self.balance * (profit_pct / 100) * lot_size
            self.balance += profit_usd
            self.equity = self.balance
            
            result = {
                'pair': pair,
                'signal': signal,
                'entry_price': round(entry_price, 5),
                'exit_price': round(tp_price if outcome == 'tp' else sl_price, 5),
                'sl_price': round(sl_price, 5),
                'tp_price': round(tp_price, 5),
                'outcome': outcome,
                'profit_pct': round(profit_pct, 2),
                'profit_usd': round(profit_usd, 2),
                'balance': round(self.balance, 2),
                'sentiment_score': sentiment_score
            }
            
            self.trades.append(result)
            results.append(result)
        
        return results
    
    def run_multi_pair_backtest(self,
                                num_signals: int = 50,
                                pairs_per_signal: int = 3,
                                lot_size: float = 0.01,
                                sl_percent: float = 1.0,
                                tp_percent: float = 10.0) -> Dict:
        """
        Run backtest dengan multi-pair trading simulation
        
        Args:
            num_signals: Number of news signals to simulate
            pairs_per_signal: Pairs to trade per signal
            lot_size: Lot size per pair
            sl_percent: Stop loss percent
            tp_percent: Take profit percent
        
        Returns:
            Backtest results
        """
        print(f"\n{'='*70}")
        print(f"🔬 RUNNING MULTI-PAIR BACKTEST SIMULATION")
        print(f"{'='*70}")
        print(f"Initial Balance: ${self.initial_balance:,.2f}")
        print(f"Number of Signals: {num_signals}")
        print(f"Pairs per Signal: {pairs_per_signal}")
        print(f"Lot Size: {lot_size}")
        print(f"SL: {sl_percent}% | TP: {tp_percent}%")
        print(f"{'='*70}\n")
        
        self.balance = self.initial_balance
        self.trades = []
        
        # Available pairs
        available_pairs = [
            'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD',
            'NZDUSD', 'USDCHF', 'EURGBP', 'EURJPY', 'GBPJPY'
        ]
        
        for i in range(num_signals):
            # Random signal
            signal = np.random.choice(['LONG', 'SHORT'])
            
            # Random sentiment score (-1 to 1)
            sentiment_score = np.random.uniform(-1, 1)
            
            # Select random pairs
            selected_pairs = np.random.choice(
                available_pairs,
                size=min(pairs_per_signal, len(available_pairs)),
                replace=False
            )
            
            # Simulate trades
            results = self.simulate_multi_pair_trade(
                list(selected_pairs),
                signal,
                lot_size,
                sl_percent,
                tp_percent,
                sentiment_score
            )
            
            if (i + 1) % 10 == 0:
                total_profit = sum(r['profit_usd'] for r in results)
                print(f"Signal {i+1}/{num_signals} - "
                      f"Pairs: {len(results)} - "
                      f"P/L: ${total_profit:.2f} - "
                      f"Balance: ${self.balance:.2f}")
        
        # Calculate final statistics
        df = pd.DataFrame(self.trades)
        
        total_profit = self.balance - self.initial_balance
        roi = (total_profit / self.initial_balance) * 100
        
        winning_trades = len(df[df['profit_usd'] > 0])
        losing_trades = len(df[df['profit_usd'] < 0])
        total_trades = len(df)
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_wins = df[df['profit_usd'] > 0]['profit_usd'].sum()
        total_losses = abs(df[df['profit_usd'] < 0]['profit_usd'].sum())
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        # Max drawdown
        df['cumulative'] = df['profit_usd'].cumsum()
        df['peak'] = df['cumulative'].cummax()
        df['drawdown'] = df['peak'] - df['cumulative']
        max_drawdown = df['drawdown'].max()
        max_drawdown_pct = (max_drawdown / self.initial_balance) * 100
        
        results = {
            'initial_balance': self.initial_balance,
            'final_balance': round(self.balance, 2),
            'total_profit': round(total_profit, 2),
            'roi': round(roi, 2),
            'total_trades': total_trades,
            'total_signals': num_signals,
            'avg_pairs_per_signal': round(total_trades / num_signals, 1),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'avg_profit': round(df['profit_usd'].mean(), 2),
            'max_profit': round(df['profit_usd'].max(), 2),
            'max_loss': round(df['profit_usd'].min(), 2),
            'max_drawdown': round(max_drawdown, 2),
            'max_drawdown_pct': round(max_drawdown_pct, 2)
        }
        
        return results
    
    def print_backtest_results(self, results: Dict):
        """Print hasil backtest dengan format yang bagus"""
        print(f"\n{'='*70}")
        print(f"📈 MULTI-PAIR BACKTEST RESULTS")
        print(f"{'='*70}")
        print(f"Initial Balance: ${results['initial_balance']:,.2f}")
        print(f"Final Balance: ${results['final_balance']:,.2f}")
        print(f"Total Profit/Loss: ${results['total_profit']:,.2f}")
        print(f"ROI: {results['roi']}%")
        print(f"-"*70)
        print(f"Total Signals: {results['total_signals']}")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Avg Pairs per Signal: {results['avg_pairs_per_signal']}")
        print(f"Winning Trades: {results['winning_trades']} ({results['win_rate']:.1f}%)")
        print(f"Losing Trades: {results['losing_trades']}")
        print(f"Profit Factor: {results['profit_factor']}")
        print(f"-"*70)
        print(f"Average P/L per Trade: ${results['avg_profit']:.2f}")
        print(f"Maximum Profit: ${results['max_profit']:.2f}")
        print(f"Maximum Loss: ${results['max_loss']:.2f}")
        print(f"Max Drawdown: ${results['max_drawdown']:.2f} ({results['max_drawdown_pct']:.1f}%)")
        print(f"{'='*70}\n")
        
        # Performance evaluation
        if results['roi'] > 50 and results['profit_factor'] > 2.0:
            print("🏆 EXCELLENT PERFORMANCE!")
            print("   - High ROI and profit factor")
            print("   - Strategy is very profitable")
        elif results['roi'] > 20 and results['profit_factor'] > 1.5:
            print("👍 GOOD PERFORMANCE")
            print("   - Positive ROI and decent profit factor")
            print("   - Strategy shows promise")
        elif results['roi'] > 0:
            print("✅ PROFITABLE")
            print("   - Positive returns but could be optimized")
        else:
            print("⚠️ NEEDS OPTIMIZATION")
            print("   - Negative returns")
            print("   - Review strategy parameters")
        print()


def main():
    """Main function untuk demo monitoring dan backtesting"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║     TRADING MONITOR & BACKTEST TOOLS - MULTI-PAIR VERSION        ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Demo Backtesting
    print("\n1️⃣  Running Multi-Pair Backtest Simulation...\n")
    
    backtest = EnhancedBacktestEngine(initial_balance=10000)
    
    results = backtest.run_multi_pair_backtest(
        num_signals=50,        # 50 news signals
        pairs_per_signal=3,    # Trade 3 pairs per signal
        lot_size=0.01,
        sl_percent=1.0,
        tp_percent=10.0
    )
    
    backtest.print_backtest_results(results)
    
    # Demo Monitoring
    print("\n2️⃣  Trading Monitor Demo...\n")
    
    monitor = TradingMonitor()
    
    # Simulate beberapa trades
    sample_trades = [
        {'symbol': 'EURUSD', 'direction': 'LONG', 'profit': 15.50, 
         'open_time': '2024-02-09 10:00', 'close_time': '2024-02-09 14:30'},
        {'symbol': 'EURUSD', 'direction': 'SHORT', 'profit': -10.20,
         'open_time': '2024-02-09 11:00', 'close_time': '2024-02-09 12:00'},
        {'symbol': 'GBPUSD', 'direction': 'LONG', 'profit': 22.30,
         'open_time': '2024-02-09 13:00', 'close_time': '2024-02-09 18:00'},
        {'symbol': 'EURUSD', 'direction': 'LONG', 'profit': 18.75,
         'open_time': '2024-02-09 15:00', 'close_time': '2024-02-09 16:30'},
        {'symbol': 'USDJPY', 'direction': 'SHORT', 'profit': -8.50,
         'open_time': '2024-02-09 16:00', 'close_time': '2024-02-09 17:00'},
        {'symbol': 'GBPUSD', 'direction': 'SHORT', 'profit': 12.80,
         'open_time': '2024-02-09 17:00', 'close_time': '2024-02-09 19:00'},
    ]
    
    for trade in sample_trades:
        monitor.log_trade(trade)
    
    monitor.print_performance_report(by_pair=True)
    
    # Weekly summary
    print("\n📅 WEEKLY SUMMARY")
    print("="*70)
    weekly = monitor.get_weekly_summary()
    print(f"{'Date':<12} {'Trades':<8} {'Wins':<8} {'Win%':<8} {'P/L':<12}")
    print("-"*70)
    for day in weekly:
        if day['trades'] > 0:
            print(f"{day['date']:<12} {day['trades']:<8} {day['wins']:<8} "
                  f"{day['win_rate']:<8.1f} ${day['profit']:<11.2f}")
    print("="*70 + "\n")
    
    # Export
    print("3️⃣  Exporting data...\n")
    monitor.export_to_csv('demo_trades.csv')
    print()


if __name__ == "__main__":
    main()
