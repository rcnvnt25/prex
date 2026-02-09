"""
Advanced Configuration Examples
Konfigurasi lanjutan untuk customize bot sesuai kebutuhan Anda
"""

# ============================================================
# CONTOH 1: CONSERVATIVE TRADING (Low Risk)
# ============================================================
conservative_config = {
    'symbol': 'EURUSD',
    'lot_size': 0.01,              # Micro lot - risiko minimal
    'stop_loss_percent': 0.5,      # SL sangat ketat (0.5%)
    'take_profit_percent': 3.0,    # TP konservatif (3%)
    'check_interval': 300,         # Check setiap 5 menit
    'min_sentiment_strength': 'strong',  # Hanya trade signal kuat
}

# ============================================================
# CONTOH 2: AGGRESSIVE TRADING (High Risk High Reward)
# ============================================================
aggressive_config = {
    'symbol': 'GBPUSD',
    'lot_size': 0.1,               # Mini lot - risiko lebih besar
    'stop_loss_percent': 2.0,      # SL lebih lebar (2%)
    'take_profit_percent': 20.0,   # TP agresif (20%)
    'check_interval': 30,          # Check setiap 30 detik
    'min_sentiment_strength': 'moderate',  # Trade moderate & strong
}

# ============================================================
# CONTOH 3: SCALPING (Quick Trades)
# ============================================================
scalping_config = {
    'symbol': 'EURUSD',
    'lot_size': 0.05,
    'stop_loss_percent': 0.3,      # SL sangat ketat
    'take_profit_percent': 0.8,    # TP kecil tapi cepat
    'check_interval': 15,          # Check setiap 15 detik
}

# ============================================================
# CONTOH 4: SWING TRADING (Longer Holds)
# ============================================================
swing_config = {
    'symbol': 'USDJPY',
    'lot_size': 0.02,
    'stop_loss_percent': 3.0,      # SL lebar untuk swing
    'take_profit_percent': 15.0,   # TP lebih besar
    'check_interval': 3600,        # Check setiap 1 jam
}

# ============================================================
# CONTOH 5: MULTI-PAIR DIVERSIFICATION
# ============================================================
multi_pair_configs = [
    {
        'symbol': 'EURUSD',
        'lot_size': 0.01,
        'stop_loss_percent': 1.0,
        'take_profit_percent': 10.0,
    },
    {
        'symbol': 'GBPUSD',
        'lot_size': 0.01,
        'stop_loss_percent': 1.0,
        'take_profit_percent': 10.0,
    },
    {
        'symbol': 'USDJPY',
        'lot_size': 0.01,
        'stop_loss_percent': 1.0,
        'take_profit_percent': 10.0,
    },
]

# ============================================================
# MONEY MANAGEMENT CALCULATOR
# ============================================================
def calculate_lot_size_from_risk(
    account_balance: float,
    risk_percent: float,
    stop_loss_pips: float,
    pip_value: float = 0.0001
) -> float:
    """
    Calculate lot size berdasarkan risk management
    
    Args:
        account_balance: Saldo akun dalam USD
        risk_percent: Persen risiko per trade (contoh: 1.0 untuk 1%)
        stop_loss_pips: Stop loss dalam pips
        pip_value: Nilai per pip (default 0.0001 untuk EURUSD)
    
    Returns:
        Lot size yang sesuai
    
    Example:
        >>> calculate_lot_size_from_risk(1000, 1.0, 50)
        0.02  # Trade dengan risiko $10 (1% dari $1000)
    """
    risk_amount = account_balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value * 100000)
    
    # Round to 2 decimal places
    lot_size = round(lot_size, 2)
    
    # Minimum lot size
    if lot_size < 0.01:
        lot_size = 0.01
    
    return lot_size

# ============================================================
# TIME-BASED TRADING FILTER
# ============================================================
trading_hours = {
    # Trading hanya saat volatilitas tinggi
    'london_session': {
        'start': '08:00',
        'end': '16:00',
        'timezone': 'Europe/London'
    },
    'new_york_session': {
        'start': '13:00',
        'end': '22:00',
        'timezone': 'America/New_York'
    },
    'tokyo_session': {
        'start': '00:00',
        'end': '09:00',
        'timezone': 'Asia/Tokyo'
    },
    # Hindari trading saat news release besar
    'avoid_news_times': [
        '15:30',  # US Session open & major data
        '14:00',  # ECB announcements
        '13:00',  # UK data releases
    ]
}

# ============================================================
# SENTIMENT THRESHOLD CONFIGURATION
# ============================================================
sentiment_thresholds = {
    'very_strong': {
        'min_score': 0.7,
        'lot_multiplier': 1.5,  # Trade lebih besar untuk signal sangat kuat
    },
    'strong': {
        'min_score': 0.4,
        'lot_multiplier': 1.0,
    },
    'moderate': {
        'min_score': 0.2,
        'lot_multiplier': 0.7,  # Trade lebih kecil untuk signal moderate
    },
    'weak': {
        'min_score': 0.0,
        'lot_multiplier': 0.0,  # Tidak trade untuk signal weak
    }
}

# ============================================================
# NEWS IMPACT FILTER
# ============================================================
news_impact_filter = {
    'high': {
        'trade': True,
        'lot_multiplier': 1.0,
    },
    'medium': {
        'trade': True,
        'lot_multiplier': 0.7,
    },
    'low': {
        'trade': False,  # Skip low impact news
        'lot_multiplier': 0.0,
    }
}

# ============================================================
# DAILY LIMITS (Circuit Breaker)
# ============================================================
daily_limits = {
    'max_trades_per_day': 10,      # Maksimal 10 trade per hari
    'max_daily_loss': 50.0,        # Stop trading jika loss $50
    'max_daily_profit': 200.0,     # Stop trading jika profit $200 (lock profit)
    'max_consecutive_losses': 3,   # Stop setelah 3 loss berturut-turut
}

# ============================================================
# BROKER-SPECIFIC SETTINGS
# ============================================================
broker_settings = {
    'IC Markets': {
        'min_lot': 0.01,
        'max_lot': 100.0,
        'spread_typical': 0.1,  # pips
    },
    'XM': {
        'min_lot': 0.01,
        'max_lot': 50.0,
        'spread_typical': 0.8,
    },
    'Pepperstone': {
        'min_lot': 0.01,
        'max_lot': 100.0,
        'spread_typical': 0.09,
    },
}

# ============================================================
# EXAMPLE: Using Advanced Configuration
# ============================================================
if __name__ == "__main__":
    # Example 1: Calculate lot size based on account
    account_balance = 1000  # $1000
    risk_per_trade = 1.0    # 1% risk
    sl_pips = 50            # 50 pips SL
    
    lot_size = calculate_lot_size_from_risk(
        account_balance, 
        risk_per_trade, 
        sl_pips
    )
    
    print(f"Recommended lot size: {lot_size}")
    print(f"Risk amount: ${account_balance * risk_per_trade / 100}")
    
    # Example 2: Print all configurations
    print("\n=== AVAILABLE CONFIGURATIONS ===")
    print(f"Conservative: {conservative_config}")
    print(f"Aggressive: {aggressive_config}")
    print(f"Scalping: {scalping_config}")
    print(f"Swing: {swing_config}")
