# 🚀 QUICK START - FOREX AI BOT

## ✅ FILE YANG ANDA TERIMA

### Core Files (WAJIB):
1. **forex_ai_bot.py** - Main bot program
2. **requirements.txt** - Python packages yang dibutuhkan
3. **.env.example** - Template konfigurasi (rename jadi .env)

### Documentation:
4. **README.md** - Dokumentasi lengkap fitur bot
5. **SETUP_GUIDE_INDONESIA.md** - Panduan setup step-by-step

### Optional (Advanced):
6. **advanced_config.py** - Konfigurasi lanjutan & presets
7. **backtest_monitor.py** - Tools untuk backtest & monitoring
8. **forex_bot_dependency_map.jsx** - Visualisasi dependency (React component)

---

## 🎯 INSTALASI CEPAT (5 LANGKAH)

### 1️⃣ Install Python Packages
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Telegram API

**Buka:** https://my.telegram.org/auth

1. Login dengan nomor HP Telegram Anda
2. Pilih "API development tools"
3. Create new application
4. **CATAT:** api_id dan api_hash

### 3️⃣ Setup MT5 Demo Account

1. Install MT5 dari broker Anda
2. Buat akun demo
3. **CATAT:** Login, Password, Server

### 4️⃣ Buat File .env

```bash
# Copy file example
cp .env.example .env

# Edit .env dengan text editor
nano .env  # atau notepad .env di Windows
```

**ISI dengan data Anda:**
```bash
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword123
MT5_SERVER=BrokerName-Demo

TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef123456...
TELEGRAM_PHONE=+628123456789

DEFAULT_LOT_SIZE=0.01
STOP_LOSS_PERCENT=1.0
TAKE_PROFIT_PERCENT=10.0
MAX_DAILY_LOSS=50.0
MAX_DAILY_PROFIT=200.0
MAX_TRADES_PER_DAY=20
```

### 5️⃣ Jalankan Bot

```bash
python forex_ai_bot.py
```

**Pertama kali:** Bot akan minta kode verifikasi dari Telegram. Check Telegram app Anda dan masukkan kode tersebut.

---

## 📱 TELEGRAM SETUP DETAIL

### Mengapa Tidak Perlu Buat Bot?

Bot ini menggunakan **Telethon** untuk **scraping channel** langsung, BUKAN Telegram Bot API.

### Cara Dapatkan API Credentials:

**Step 1:** Buka https://my.telegram.org/auth
```
┌─────────────────────────────────┐
│  Phone number                   │
│  [+62 812 3456 789]            │
│                                 │
│  [      Next      ]            │
└─────────────────────────────────┘
```

**Step 2:** Masukkan kode dari Telegram
```
Check your Telegram app!
Code: [12345]
```

**Step 3:** API Development Tools
```
┌─────────────────────────────────┐
│  App title: Forex AI Bot       │
│  Short name: forexbot           │
│  Platform: Other                │
│                                 │
│  [  Create application  ]      │
└─────────────────────────────────┘
```

**Step 4:** COPY CREDENTIALS
```
✅ api_id: 12345678
✅ api_hash: abcdef1234567890abcdef...
```

### Join Channels Dulu!

Sebelum run bot, **WAJIB join** dulu:
- https://t.me/marketfeed
- https://t.me/wfwitness

---

## 🎮 CARA KERJA BOT

### Flow Diagram:
```
Telegram Channels
(@marketfeed, @wfwitness)
        ↓
Bot scrapes new messages
        ↓
AI Sentiment Analysis
        ↓
Score: -1.0 to +1.0
        ↓
┌─────────────┬──────────────┐
│ Score > 0.3 │ Score < -0.3 │
│   LONG      │    SHORT     │
└─────────────┴──────────────┘
        ↓
Detect affected currency
        ↓
Select pairs to trade
        ↓
OPEN POSITIONS
        ↓
Monitor with SL/TP
```

### Example:

**News:** "EUR surges on positive ECB outlook"

1. **Sentiment Analysis:**
   - Keywords: "surges", "positive", "outlook"
   - Score: +0.68 (Strong Bullish)
   - Signal: LONG

2. **Currency Detection:**
   - Affected: EUR, USD

3. **Pair Selection:**
   - EURUSD, EURJPY, EURGBP, EURAUD

4. **Execution:**
   - OPEN LONG pada semua 4 pairs
   - SL: -1%
   - TP: +10%

---

## ⚙️ KONFIGURASI PENTING

### Lot Size
```bash
DEFAULT_LOT_SIZE=0.01  # Micro lot (safe untuk demo $10k)
```
- 0.01 = Micro lot ($1000)
- 0.1 = Mini lot ($10,000)
- 1.0 = Standard lot ($100,000)

**Recommendation:** Start dengan 0.01!

### Stop Loss & Take Profit
```bash
STOP_LOSS_PERCENT=1.0    # Auto close jika minus 1%
TAKE_PROFIT_PERCENT=10.0  # Auto close jika profit 10%
```

**Risk/Reward Ratio:** 1:10 (bagus!)

### Daily Limits (Circuit Breaker)
```bash
MAX_DAILY_LOSS=50.0       # Stop trading jika loss $50
MAX_DAILY_PROFIT=200.0    # Lock profit jika profit $200
MAX_TRADES_PER_DAY=20     # Max 20 trades per hari
```

**Proteksi** dari over-trading dan big losses!

---

## 🔍 MONITORING

### Real-time Output:
```
⏰ 2024-02-09 10:15:30

📊 Monitoring 3 open position(s)...
🟢 EURUSD #123: +2.5% | P/L: $25.00 | Price: 1.08830
🟢 GBPUSD #124: +1.8% | P/L: $18.00 | Price: 1.26950
🔴 USDJPY #125: -0.4% | P/L: -$4.00 | Price: 110.125
💰 Total Floating P/L: $39.00

📱 Fetching news from Telegram channels...
   No new messages

💤 Waiting 60 seconds for next check...
```

### Performance Report:
```bash
python backtest_monitor.py
```

Output:
```
📊 TRADING PERFORMANCE REPORT
════════════════════════════════════
Total Trades: 45
Winning Trades: 28 (62.2%)
Losing Trades: 17 (37.8%)
Profit Factor: 2.15
Total P/L: $450.00
Average Win: $25.30
Average Loss: -$12.80
Win Rate: 62.2%
🏆 EXCELLENT PERFORMANCE
```

---

## ⚠️ SAFETY TIPS

### ✅ DO's:
- ✅ Start with **DEMO account**
- ✅ Use **small lot sizes** (0.01)
- ✅ Set **strict daily limits**
- ✅ Monitor **regularly**
- ✅ Test **1-2 bulan** dulu
- ✅ Keep MT5 **terminal open**
- ✅ Check **internet connection**

### ❌ DON'T's:
- ❌ Langsung ke live account
- ❌ Use lot size terlalu besar
- ❌ No daily limits
- ❌ Set and forget
- ❌ Trade dengan uang yang tidak bisa hilang
- ❌ Close MT5 saat bot running

---

## 🛠️ TROUBLESHOOTING CEPAT

### Bot tidak jalan?
```bash
# Check Python version
python --version  # Harus 3.8+

# Check packages installed
pip list | grep MetaTrader5
pip list | grep telethon

# Re-install jika perlu
pip install -r requirements.txt --force-reinstall
```

### MT5 error?
```bash
# 1. Check MT5 running
# 2. Check sudah login
# 3. Enable algo trading:
#    Tools -> Options -> Expert Advisors
#    ✅ Allow automated trading
```

### Telegram error?
```bash
# Delete session dan login ulang
rm forex_bot_session.session
python forex_ai_bot.py
# Enter verification code lagi
```

### Tidak dapat news?
```bash
# 1. Join channel dulu:
#    https://t.me/marketfeed
#    https://t.me/wfwitness
#
# 2. Check TELEGRAM_API_ID di .env
# 3. Check internet connection
```

---

## 📚 NEXT STEPS

### Minggu 1-2: Learning
- Run di demo account
- Observe bot behavior
- Understand sentiment analysis
- Monitor positions

### Minggu 3-4: Optimization
- Analyze performance
- Adjust parameters if needed
- Test different lot sizes
- Fine-tune limits

### Minggu 5+: Advanced
- Try different pair groups
- Test time-based filters
- Optimize SL/TP ratios
- Consider live trading (jika profitable!)

---

## 📞 NEED HELP?

### Priority Order:
1. ✅ Read **SETUP_GUIDE_INDONESIA.md** (lengkap!)
2. ✅ Check **Troubleshooting** section
3. ✅ Test individual components
4. ✅ Review **.env** configuration
5. ✅ Restart everything (MT5, bot)

### Files to Check:
- `.env` - Configuration
- `forex_bot_session.session` - Telegram session
- `trading_log.json` - Trade history

---

## 🎯 SUCCESS METRICS

### After 1 Month Demo:
- [ ] Win rate > 50%
- [ ] Profit factor > 1.5
- [ ] Consistent daily profits
- [ ] No major drawdowns
- [ ] Understand bot behavior

### Ready for Live Trading:
- [ ] 2+ months profitable in demo
- [ ] Win rate > 55%
- [ ] Profit factor > 2.0
- [ ] Confident with risk management
- [ ] Emotional discipline ready

---

**🚀 GOOD LUCK!**

**Remember:** Patience + Discipline = Profit

**Trade smart, not hard! 💪**

---

## 📝 QUICK REFERENCE

### Start Bot:
```bash
python forex_ai_bot.py
```

### Stop Bot:
```
Ctrl + C
```

### Check Performance:
```bash
python backtest_monitor.py
```

### Re-login Telegram:
```bash
rm forex_bot_session.session
python forex_ai_bot.py
```

### Update Packages:
```bash
pip install -r requirements.txt --upgrade
```

---

**Version:** 2.0 - Multi-Pair + Telegram Integration  
**Last Updated:** February 2024
