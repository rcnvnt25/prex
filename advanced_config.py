"""
Advanced Configuration Examples - UPGRADED VERSION
Konfigurasi lanjutan untuk multi-pair trading dengan Telegram news
"""

import os
from typing import Dict, List

# ============================================================
# CONTOH 1: CONSERVATIVE TRADING (Low Risk)
# ============================================================
conservative_config = {
    'lot_size': 0.01,              # Micro lot - risiko minimal
    'stop_loss_percent': 0.5,      # SL sangat ketat (0.5%)
    'take_profit_percent': 3.0,    # TP konservatif (3%)
    'check_interval': 300,         # Check setiap 5 menit
    'max_daily_trades': 5,         # Limit trades
    'max_daily_loss': 25.0,        # Loss limit kecil
}

# ============================================================
# CONTOH 2: AGGRESSIVE TRADING (High Risk High Reward)
# ============================================================
aggressive_config = {
    'lot_size': 0.1,               # Mini lot - risiko lebih besar
    'stop_loss_percent': 2.0,      # SL lebih lebar (2%)
    'take_profit_percent': 20.0,   # TP agresif (20%)
    'check_interval': 30,          # Check setiap 30 detik
    'max_daily_trades': 50,        # Banyak trades
    'max_daily_loss': 100.0,       # Loss limit besar
}

# ============================================================
# CONTOH 3: BALANCED (Recommended)
# ============================================================
balanced_config = {
    'lot_size': 0.02,
    'stop_loss_percent': 1.0,
    'take_profit_percent': 10.0,
    'check_interval': 60,
    'max_daily_trades': 20,
    'max_daily_loss': 50.0,
    'max_daily_profit': 200.0,
}

# ============================================================
# PAIR GROUPS untuk selective trading
# ============================================================
pair_groups = {
    'majors': [
        'EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF',
        'AUDUSD', 'USDCAD', 'NZDUSD'
    ],
    'minors': [
        'EURGBP', 'EURJPY', 'GBPJPY', 'EURCHF',
        'EURAUD', 'EURCAD', 'GBPAUD', 'GBPCAD'
    ],
    'exotics': [
        'USDTRY', 'USDZAR', 'USDMXN', 'USDHKD'
    ],
    # High volatility pairs
    'volatile': [
        'GBPJPY', 'GBPAUD', 'GBPNZD', 'EURJPY'
    ],
    # Low spread pairs (good for scalping)
    'low_spread': [
        'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF'
    ]
}

# ============================================================
# SENTIMENT STRENGTH THRESHOLDS
# ============================================================
sentiment_config = {
    'very_strong': {
        'min_score': 0.7,           # Sentiment score >= 0.7
        'lot_multiplier': 1.5,      # Trade lebih besar
        'trade': True
    },
    'strong': {
        'min_score': 0.5,
        'lot_multiplier': 1.0,      # Normal lot size
        'trade': True
    },
    'moderate': {
        'min_score': 0.3,
        'lot_multiplier': 0.7,      # Trade lebih kecil
        'trade': True               # Set False jika hanya mau trade strong+
    },
    'weak': {
        'min_score': 0.0,
        'lot_multiplier': 0.0,
        'trade': False              # Skip weak signals
    }
}

# ============================================================
# TIME-BASED FILTERS
# ============================================================
trading_sessions = {
    'tokyo': {
        'start': '00:00',
        'end': '09:00',
        'timezone': 'Asia/Tokyo',
        'active': True,             # Set False to skip
        'pairs': ['USDJPY', 'AUDJPY', 'EURJPY', 'GBPJPY']
    },
    'london': {
        'start': '08:00',
        'end': '16:00',
        'timezone': 'Europe/London',
        'active': True,
        'pairs': ['EURGBP', 'EURUSD', 'GBPUSD']
    },
    'new_york': {
        'start': '13:00',
        'end': '22:00',
        'timezone': 'America/New_York',
        'active': True,
        'pairs': ['EURUSD', 'GBPUSD', 'USDCAD']
    },
    'overlap_london_ny': {
        'start': '13:00',
        'end': '16:00',
        'timezone': 'Europe/London',
        'active': True,
        'pairs': 'all',             # Highest volatility
        'description': 'Best time to trade - highest volume'
    }
}

# ============================================================
# CURRENCY-SPECIFIC SETTINGS
# ============================================================
currency_settings = {
    'EUR': {
        'importance': 'high',
        'keywords': ['ecb', 'draghi', 'lagarde', 'eurozone', 'european central bank'],
        'economic_indicators': ['gdp', 'cpi', 'unemployment', 'pmi']
    },
    'USD': {
        'importance': 'high',
        'keywords': ['fed', 'powell', 'yellen', 'federal reserve', 'us economy'],
        'economic_indicators': ['nfp', 'cpi', 'gdp', 'unemployment', 'interest rate']
    },
    'GBP': {
        'importance': 'medium',
        'keywords': ['boe', 'bank of england', 'brexit', 'uk economy'],
        'economic_indicators': ['gdp', 'inflation', 'unemployment']
    },
    'JPY': {
        'importance': 'medium',
        'keywords': ['boj', 'kuroda', 'bank of japan', 'yen'],
        'economic_indicators': ['tankan', 'cpi', 'gdp']
    }
}

# ============================================================
# BROKER-SPECIFIC SETTINGS
# ============================================================
broker_configs = {
    'ic_markets': {
        'min_lot': 0.01,
        'max_lot': 100.0,
        'typical_spread_eurusd': 0.1,  # pips
        'commission_per_lot': 3.5,     # USD
        'leverage_available': [1, 30, 100, 200, 500],
        'recommended_pairs': pair_groups['majors'] + pair_groups['minors']
    },
    'xm': {
        'min_lot': 0.01,
        'max_lot': 50.0,
        'typical_spread_eurusd': 0.8,
        'commission_per_lot': 0.0,     # Zero commission
        'leverage_available': [1, 50, 100, 200, 500, 888],
        'recommended_pairs': pair_groups['majors']
    },
    'pepperstone': {
        'min_lot': 0.01,
        'max_lot': 100.0,
        'typical_spread_eurusd': 0.09,
        'commission_per_lot': 3.5,
        'leverage_available': [1, 30, 100, 200, 400, 500],
        'recommended_pairs': pair_groups['majors'] + pair_groups['low_spread']
    }
}

# ============================================================
# NEWS EVENT FILTERS
# ============================================================
news_importance_levels = {
    'critical': {
        'keywords': [
            'interest rate decision', 'nfp', 'non-farm payroll',
            'central bank meeting', 'gdp', 'cpi', 'inflation'
        ],
        'action': 'trade_immediately',
        'lot_multiplier': 1.5
    },
    'high': {
        'keywords': [
            'unemployment', 'retail sales', 'manufacturing',
            'economic outlook', 'policy decision'
        ],
        'action': 'trade_normally',
        'lot_multiplier': 1.0
    },
    'medium': {
        'keywords': [
            'statement', 'forecast', 'survey', 'index'
        ],
        'action': 'trade_cautiously',
        'lot_multiplier': 0.7
    },
    'low': {
        'keywords': [
            'opinion', 'analyst', 'market watch'
        ],
        'action': 'skip',
        'lot_multiplier': 0.0
    }
}

# ============================================================
# TELEGRAM CHANNEL WEIGHTS
# ============================================================
telegram_sources = {
    'marketfeed': {
        'weight': 1.0,              # Full weight
        'reliability': 'high',
        'focus': 'breaking news',
        'filter_retweets': True
    },
    'wfwitness': {
        'weight': 0.8,              # Slightly lower weight
        'reliability': 'medium-high',
        'focus': 'analysis',
        'filter_retweets': True
    }
}

# ============================================================
# POSITION MANAGEMENT RULES
# ============================================================
position_management = {
    'max_positions_per_pair': 1,    # Only 1 position per pair
    'max_positions_total': 10,      # Max 10 positions at once
    'max_correlated_pairs': 3,      # Max 3 correlated pairs (e.g. EURUSD, GBPUSD, EURGBP)
    'close_opposite_on_new_signal': True,  # Close LONG if new SHORT signal
    'partial_close_enabled': False, # Set True untuk take partial profits
    'partial_close_at_percent': 5.0,  # Close 50% at 5% profit
    'trailing_stop_enabled': False, # Set True untuk trailing SL
    'trailing_stop_distance': 0.5   # 0.5% trailing distance
}

# ============================================================
# DAILY LIMITS (Circuit Breaker)
# ============================================================
daily_limits_strict = {
    'max_trades_per_day': 10,
    'max_daily_loss': 30.0,        # Very strict
    'max_daily_profit': 100.0,     # Lock profit earlier
    'max_consecutive_losses': 2,   # Stop after 2 losses
    'max_drawdown_percent': 10.0,  # Max 10% drawdown
}

daily_limits_relaxed = {
    'max_trades_per_day': 30,
    'max_daily_loss': 100.0,
    'max_daily_profit': 500.0,
    'max_consecutive_losses': 5,
    'max_drawdown_percent': 20.0,
}

# ============================================================
# MONEY MANAGEMENT FUNCTIONS
# ============================================================
def calculate_lot_size_from_risk(
    account_balance: float,
    risk_percent: float,
    stop_loss_pips: float,
    pip_value: float = 10.0  # For standard lot
) -> float:
    """
    Calculate lot size based on account risk
    
    Args:
        account_balance: Balance dalam USD
        risk_percent: Risk per trade (1.0 = 1%)
        stop_loss_pips: SL dalam pips
        pip_value: Nilai per pip (10 for standard, 1 for mini, 0.1 for micro)
    
    Returns:
        Recommended lot size
    
    Example:
        >>> calculate_lot_size_from_risk(10000, 1.0, 50, 1.0)
        2.0  # 2.0 mini lots
    """
    risk_amount = account_balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    
    # Round to 2 decimals
    lot_size = round(lot_size, 2)
    
    # Minimum 0.01
    if lot_size < 0.01:
        lot_size = 0.01
    
    return lot_size


def get_optimal_pairs_for_currency(currency: str, signal: str) -> List[str]:
    """
    Get optimal pairs to trade based on currency and signal
    
    Args:
        currency: Currency code (e.g. 'EUR', 'USD')
        signal: 'LONG' or 'SHORT'
    
    Returns:
        List of recommended pairs
    
    Example:
        >>> get_optimal_pairs_for_currency('EUR', 'LONG')
        ['EURUSD', 'EURJPY', 'EURGBP']  # Buy EUR against others
    """
    major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD']
    pairs = []
    
    if signal == 'LONG':
        # Buy the currency - so it should be base currency
        for other in major_currencies:
            if currency != other:
                pair = f"{currency}{other}"
                pairs.append(pair)
    else:  # SHORT
        # Sell the currency - so it should be quote currency
        for other in major_currencies:
            if currency != other:
                pair = f"{other}{currency}"
                pairs.append(pair)
    
    return pairs


def filter_by_correlation(pairs: List[str], max_correlated: int = 3) -> List[str]:
    """
    Filter pairs to avoid too many correlated positions
    
    Args:
        pairs: List of pairs to trade
        max_correlated: Max number of correlated pairs
    
    Returns:
        Filtered list of pairs
    """
    # Simple correlation groups
    correlation_groups = {
        'eur_group': ['EURUSD', 'EURGBP', 'EURJPY', 'EURAUD'],
        'usd_group': ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD'],
        'jpy_group': ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY'],
        'gbp_group': ['GBPUSD', 'EURGBP', 'GBPJPY', 'GBPAUD']
    }
    
    # Count how many pairs from each group
    selected = []
    group_counts = {group: 0 for group in correlation_groups}
    
    for pair in pairs:
        # Check which groups this pair belongs to
        can_add = True
        for group_name, group_pairs in correlation_groups.items():
            if pair in group_pairs:
                if group_counts[group_name] >= max_correlated:
                    can_add = False
                    break
        
        if can_add:
            selected.append(pair)
            # Update group counts
            for group_name, group_pairs in correlation_groups.items():
                if pair in group_pairs:
                    group_counts[group_name] += 1
    
    return selected


# ============================================================
# PRESET CONFIGURATIONS
# ============================================================
PRESETS = {
    'conservative': {
        **conservative_config,
        'pair_groups': pair_groups['low_spread'],
        'sentiment_threshold': 'strong',
        'daily_limits': daily_limits_strict
    },
    'balanced': {
        **balanced_config,
        'pair_groups': pair_groups['majors'],
        'sentiment_threshold': 'moderate',
        'daily_limits': daily_limits_relaxed
    },
    'aggressive': {
        **aggressive_config,
        'pair_groups': pair_groups['majors'] + pair_groups['volatile'],
        'sentiment_threshold': 'moderate',
        'daily_limits': daily_limits_relaxed
    }
}


# ============================================================
# EXAMPLE: Loading Configuration
# ============================================================
def load_config(preset: str = 'balanced') -> Dict:
    """
    Load configuration preset
    
    Args:
        preset: 'conservative', 'balanced', or 'aggressive'
    
    Returns:
        Configuration dictionary
    """
    if preset not in PRESETS:
        print(f"⚠️ Unknown preset '{preset}', using 'balanced'")
        preset = 'balanced'
    
    config = PRESETS[preset].copy()
    
    # Override dengan .env jika ada
    if os.getenv('DEFAULT_LOT_SIZE'):
        config['lot_size'] = float(os.getenv('DEFAULT_LOT_SIZE'))
    
    if os.getenv('STOP_LOSS_PERCENT'):
        config['stop_loss_percent'] = float(os.getenv('STOP_LOSS_PERCENT'))
    
    if os.getenv('TAKE_PROFIT_PERCENT'):
        config['take_profit_percent'] = float(os.getenv('TAKE_PROFIT_PERCENT'))
    
    return config


if __name__ == "__main__":
    # Demo usage
    print("=== ADVANCED CONFIGURATION DEMO ===\n")
    
    # Example 1: Calculate lot size
    print("1. Calculate lot size based on risk:")
    lot_size = calculate_lot_size_from_risk(
        account_balance=10000,
        risk_percent=1.0,
        stop_loss_pips=50,
        pip_value=1.0
    )
    print(f"   Recommended lot size: {lot_size}")
    print(f"   Risk: $100 (1% of $10,000)\n")
    
    # Example 2: Get optimal pairs
    print("2. Optimal pairs for EUR bullish:")
    pairs = get_optimal_pairs_for_currency('EUR', 'LONG')
    print(f"   {', '.join(pairs[:5])}\n")
    
    # Example 3: Filter by correlation
    print("3. Filter correlated pairs:")
    all_pairs = ['EURUSD', 'GBPUSD', 'EURGBP', 'USDJPY', 'EURJPY']
    filtered = filter_by_correlation(all_pairs, max_correlated=2)
    print(f"   Input: {', '.join(all_pairs)}")
    print(f"   Filtered: {', '.join(filtered)}\n")
    
    # Example 4: Load preset
    print("4. Load 'balanced' preset:")
    config = load_config('balanced')
    print(f"   Lot size: {config['lot_size']}")
    print(f"   SL: {config['stop_loss_percent']}%")
    print(f"   TP: {config['take_profit_percent']}%")
    print(f"   Max daily trades: {config['max_daily_trades']}")
