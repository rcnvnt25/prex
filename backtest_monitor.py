"""
Backtesting & Monitoring Tools
Tools untuk test performance bot dan monitor trading
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import json


class TradingMonitor:
    """Monitor dan track performance trading bot"""
    
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
        except FileNotFoundError:
            self.trades_history = []
    
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
    
    def get_performance_stats(self) -> Dict:
        """
        Calculate performance statistics
        
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
        
        df = pd.DataFrame(self.trades_history)
        
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
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'total_profit': round(total_profit, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'largest_win': round(df['profit'].max(), 2) if total_trades > 0 else 0,
            'largest_loss': round(df['profit'].min(), 2) if total_trades > 0 else 0,
        }
    
    def print_performance_report(self):
        """Print detailed performance report"""
        stats = self.get_performance_stats()
        
        print("\n" + "="*60)
        print("📊 TRADING PERFORMANCE REPORT")
        print("="*60)
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Winning Trades: {stats['winning_trades']}")
        print(f"Losing Trades: {stats['losing_trades']}")
        print(f"Win Rate: {stats['win_rate']}%")
        print(f"Profit Factor: {stats['profit_factor']}")
        print(f"-"*60)
        print(f"Total Profit/Loss: ${stats['total_profit']}")
        print(f"Average Win: ${stats['avg_win']}")
        print(f"Average Loss: ${stats['avg_loss']}")
        print(f"Largest Win: ${stats['largest_win']}")
        print(f"Largest Loss: ${stats['largest_loss']}")
        print("="*60 + "\n")
    
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
            if t['timestamp'].startswith(date_str)
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
        }


class BacktestEngine:
    """Engine untuk backtest strategi trading"""
    
    def __init__(self, symbol: str, initial_balance: float = 10000):
        """
        Initialize Backtest Engine
        
        Args:
            symbol: Trading pair
            initial_balance: Modal awal untuk backtest
        """
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
    
    def fetch_historical_data(self, days: int = 30) -> pd.DataFrame:
        """
        Fetch historical price data dari MT5
        
        Args:
            days: Jumlah hari data yang akan diambil
            
        Returns:
            DataFrame berisi OHLC data
        """
        if not mt5.initialize():
            print("Failed to initialize MT5")
            return pd.DataFrame()
        
        # Get rates
        rates = mt5.copy_rates_from_pos(
            self.symbol,
            mt5.TIMEFRAME_H1,  # 1 hour timeframe
            0,
            days * 24
        )
        
        mt5.shutdown()
        
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        return df
    
    def simulate_trade(self, 
                      entry_price: float,
                      direction: str,
                      lot_size: float,
                      sl_percent: float,
                      tp_percent: float) -> Dict:
        """
        Simulate single trade
        
        Args:
            entry_price: Harga entry
            direction: 'BUY' atau 'SELL'
            lot_size: Ukuran lot
            sl_percent: Stop loss dalam persen
            tp_percent: Take profit dalam persen
            
        Returns:
            Dictionary berisi hasil trade
        """
        if direction == 'BUY':
            sl_price = entry_price * (1 - sl_percent / 100)
            tp_price = entry_price * (1 + tp_percent / 100)
        else:
            sl_price = entry_price * (1 + sl_percent / 100)
            tp_price = entry_price * (1 - tp_percent / 100)
        
        # Simulate dengan asumsi random walk
        # Dalam production, gunakan historical price movement
        outcome = np.random.choice(['tp', 'sl'], p=[0.6, 0.4])  # 60% TP, 40% SL
        
        if outcome == 'tp':
            profit_pct = tp_percent if direction == 'BUY' else -tp_percent
            exit_price = tp_price
        else:
            profit_pct = -sl_percent if direction == 'BUY' else sl_percent
            exit_price = sl_price
        
        profit_usd = self.balance * (profit_pct / 100) * lot_size
        self.balance += profit_usd
        
        trade_result = {
            'direction': direction,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'outcome': outcome,
            'profit_pct': profit_pct,
            'profit_usd': round(profit_usd, 2),
            'balance': round(self.balance, 2),
        }
        
        self.trades.append(trade_result)
        return trade_result
    
    def run_backtest(self, 
                    num_trades: int = 100,
                    lot_size: float = 0.01,
                    sl_percent: float = 1.0,
                    tp_percent: float = 10.0) -> Dict:
        """
        Run full backtest simulation
        
        Args:
            num_trades: Jumlah trades untuk simulate
            lot_size: Ukuran lot per trade
            sl_percent: Stop loss persen
            tp_percent: Take profit persen
            
        Returns:
            Dictionary berisi hasil backtest
        """
        print(f"\n{'='*60}")
        print(f"🔬 RUNNING BACKTEST SIMULATION")
        print(f"{'='*60}")
        print(f"Initial Balance: ${self.initial_balance}")
        print(f"Number of Trades: {num_trades}")
        print(f"Lot Size: {lot_size}")
        print(f"SL: {sl_percent}% | TP: {tp_percent}%")
        print(f"{'='*60}\n")
        
        self.balance = self.initial_balance
        self.trades = []
        
        # Simulate trades
        base_price = 1.0850  # EURUSD base price
        
        for i in range(num_trades):
            # Random direction based on sentiment (simplified)
            direction = np.random.choice(['BUY', 'SELL'])
            
            # Simulate price variation
            entry_price = base_price + np.random.uniform(-0.01, 0.01)
            
            result = self.simulate_trade(
                entry_price, 
                direction, 
                lot_size,
                sl_percent,
                tp_percent
            )
            
            if (i + 1) % 20 == 0:
                print(f"Trade {i+1}/{num_trades} - Balance: ${result['balance']:.2f}")
        
        # Calculate statistics
        df = pd.DataFrame(self.trades)
        
        total_profit = self.balance - self.initial_balance
        roi = (total_profit / self.initial_balance) * 100
        
        winning_trades = len(df[df['profit_usd'] > 0])
        losing_trades = len(df[df['profit_usd'] < 0])
        win_rate = (winning_trades / num_trades) * 100
        
        results = {
            'initial_balance': self.initial_balance,
            'final_balance': round(self.balance, 2),
            'total_profit': round(total_profit, 2),
            'roi': round(roi, 2),
            'total_trades': num_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'avg_profit': round(df['profit_usd'].mean(), 2),
            'max_profit': round(df['profit_usd'].max(), 2),
            'max_loss': round(df['profit_usd'].min(), 2),
        }
        
        return results
    
    def print_backtest_results(self, results: Dict):
        """Print hasil backtest dengan format yang bagus"""
        print(f"\n{'='*60}")
        print(f"📈 BACKTEST RESULTS")
        print(f"{'='*60}")
        print(f"Initial Balance: ${results['initial_balance']:,.2f}")
        print(f"Final Balance: ${results['final_balance']:,.2f}")
        print(f"Total Profit/Loss: ${results['total_profit']:,.2f}")
        print(f"ROI: {results['roi']}%")
        print(f"-"*60)
        print(f"Total Trades: {results['total_trades']}")
        print(f"Winning Trades: {results['winning_trades']}")
        print(f"Losing Trades: {results['losing_trades']}")
        print(f"Win Rate: {results['win_rate']}%")
        print(f"-"*60)
        print(f"Average Profit per Trade: ${results['avg_profit']}")
        print(f"Maximum Profit: ${results['max_profit']}")
        print(f"Maximum Loss: ${results['max_loss']}")
        print(f"{'='*60}\n")
        
        # Performance evaluation
        if results['roi'] > 50:
            print("🎉 EXCELLENT PERFORMANCE!")
        elif results['roi'] > 20:
            print("👍 GOOD PERFORMANCE")
        elif results['roi'] > 0:
            print("✅ PROFITABLE")
        else:
            print("⚠️  NEEDS OPTIMIZATION")


def main():
    """Main function untuk demo monitoring dan backtesting"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         TRADING MONITOR & BACKTEST TOOLS                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Demo Backtesting
    print("\n1️⃣  Running Backtest Simulation...\n")
    
    backtest = BacktestEngine(symbol='EURUSD', initial_balance=10000)
    
    results = backtest.run_backtest(
        num_trades=100,
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
        {'symbol': 'EURUSD', 'direction': 'BUY', 'profit': 15.50},
        {'symbol': 'EURUSD', 'direction': 'SELL', 'profit': -10.20},
        {'symbol': 'GBPUSD', 'direction': 'BUY', 'profit': 22.30},
        {'symbol': 'EURUSD', 'direction': 'BUY', 'profit': 18.75},
        {'symbol': 'USDJPY', 'direction': 'SELL', 'profit': -8.50},
    ]
    
    for trade in sample_trades:
        monitor.log_trade(trade)
    
    monitor.print_performance_report()
    
    # Daily summary
    daily = monitor.get_daily_summary()
    print(f"Today's Summary: {daily['trades']} trades, ${daily['profit']} profit\n")


if __name__ == "__main__":
    main()
