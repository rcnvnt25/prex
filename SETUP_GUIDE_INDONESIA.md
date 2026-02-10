# 🚀 PANDUAN SETUP LENGKAP - FOREX AI BOT

## 📋 Daftar Isi
1. [Persyaratan System](#persyaratan-system)
2. [Instalasi](#instalasi)
3. [Setup Telegram API](#setup-telegram-api)
4. [Setup MetaTrader 5](#setup-metatrader-5)
5. [Konfigurasi Bot](#konfigurasi-bot)
6. [Menjalankan Bot](#menjalankan-bot)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ Persyaratan System

### Software yang Dibutuhkan:
- ✅ **Python 3.8 atau lebih baru**
- ✅ **MetaTrader 5 Terminal**
- ✅ **Akun MT5 Demo** (untuk testing)
- ✅ **Akun Telegram** (untuk scraping news)

### Operating System:
- ✅ Windows 10/11 (Recommended)
- ⚠️ Linux (via Wine)
- ⚠️ macOS (via Virtual Machine)

---

## 📦 Instalasi

### Langkah 1: Clone/Download Project
```bash
# Download semua file ke folder project
cd forex-ai-bot
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manual satu-satu:
```bash
pip install MetaTrader5
pip install pandas numpy
pip install python-dotenv
pip install telethon
pip install cryptg  # Opsional, untuk speed boost
```

### Langkah 3: Verify Installation
```bash
python -c "import MetaTrader5 as mt5; print('MT5:', mt5.__version__)"
python -c "from telethon import TelegramClient; print('Telethon: OK')"
```

---

## 📱 Setup Telegram API

**PENTING:** Bot ini TIDAK memerlukan Telegram Bot Token!  
Kita pakai Telethon untuk scraping channel langsung.

### Langkah-langkah:

#### 1. Dapatkan API ID dan API Hash

1. Buka browser dan kunjungi: **https://my.telegram.org/auth**

2. **Login dengan nomor HP Anda**
   - Masukkan nomor HP (format: +628123456789)
   - Klik "Next"
   - Masukkan kode konfirmasi yang dikirim ke Telegram Anda

3. **Buat Application**
   - Setelah login, pilih **"API development tools"**
   - Isi form:
     - App title: `Forex AI Bot` (atau nama apapun)
     - Short name: `forexbot`
     - Platform: Pilih `Other`
   - Klik **"Create application"**

4. **Copy Credentials**
   - Anda akan dapat:
     - `api_id` → angka (contoh: 12345678)
     - `api_hash` → string panjang (contoh: abcdef123...)
   - **SIMPAN** credentials ini!

#### 2. Screenshot untuk Panduan

```
my.telegram.org/auth
    ↓
[+62 812 3456 789] → Next
    ↓
[Masukkan kode dari Telegram]
    ↓
API development tools
    ↓
[Isi form aplikasi]
    ↓
✅ api_id: 12345678
✅ api_hash: abcdef1234567890...
```

#### 3. Test Telegram Connection

Buat file `test_telegram.py`:

```python
from telethon import TelegramClient
import asyncio

api_id = 12345678  # Ganti dengan api_id Anda
api_hash = 'abcdef123...'  # Ganti dengan api_hash Anda
phone = '+628123456789'  # Ganti dengan nomor HP Anda

async def main():
    client = TelegramClient('test_session', api_id, api_hash)
    await client.start(phone=phone)
    print("✅ Connected to Telegram!")
    
    # Test get messages from channel
    async for message in client.iter_messages('marketfeed', limit=5):
        print(f"📰 {message.date}: {message.text[:100]}...")
    
    await client.disconnect()

asyncio.run(main())
```

Jalankan:
```bash
python test_telegram.py
```

**Pertama kali:** Anda akan diminta:
1. Masukkan nomor HP
2. Masukkan kode verifikasi dari Telegram
3. (Opsional) Masukkan password 2FA jika ada

Setelah berhasil, file `forex_bot_session.session` akan dibuat.  
File ini menyimpan login session Anda (jangan di-share!).

---

## 📊 Setup MetaTrader 5

### Langkah 1: Download & Install MT5

1. **Download MT5:**
   - Kunjungi: https://www.metatrader5.com/en/download
   - Atau download dari broker Anda langsung

2. **Install MT5:**
   - Jalankan installer
   - Ikuti wizard instalasi
   - Biarkan di lokasi default: `C:\Program Files\MetaTrader 5\`

### Langkah 2: Buat Akun Demo

1. **Buka MT5 Terminal**

2. **File → Open an Account**

3. **Pilih Broker:**
   - Cari broker yang Anda inginkan (contoh: IC Markets, XM, Pepperstone)
   - Atau gunakan broker default

4. **Pilih "Open a demo account"**

5. **Isi Data:**
   - Name: Nama Anda
   - Email: Email Anda
   - Phone: Nomor HP
   - **Account Type:** Pilih yang spread rendah (contoh: Raw Spread atau ECN)
   - **Deposit:** $10,000 (untuk testing)
   - **Leverage:** 1:500 (standard)
   - **Currency:** USD

6. **Klik "Next" dan "Finish"**

7. **CATAT CREDENTIALS:**
   ```
   Login: 12345678
   Password: abcd1234
   Server: BrokerName-Demo
   ```

### Langkah 3: Enable Algo Trading

1. **Tools → Options**

2. **Tab "Expert Advisors":**
   - ✅ Centang **"Allow automated trading"**
   - ✅ Centang **"Allow DLL imports"**
   - ✅ Centang **"Allow WebRequest"** (untuk news API)

3. **Klik "OK"**

### Langkah 4: Test MT5 Connection

Buat file `test_mt5.py`:

```python
import MetaTrader5 as mt5

# Initialize
if not mt5.initialize():
    print("❌ Failed to initialize MT5")
    quit()

print("✅ MT5 initialized successfully!")

# Get account info
account_info = mt5.account_info()
if account_info:
    print(f"Login: {account_info.login}")
    print(f"Balance: ${account_info.balance}")
    print(f"Server: {account_info.server}")

# Get available symbols
symbols = mt5.symbols_get()
print(f"\n✅ Found {len(symbols)} symbols")

# Show some forex pairs
forex_pairs = [s.name for s in symbols if len(s.name) == 6 and 'USD' in s.name][:10]
print(f"Sample forex pairs: {', '.join(forex_pairs)}")

mt5.shutdown()
```

Jalankan:
```bash
python test_mt5.py
```

---

## ⚙️ Konfigurasi Bot

### Langkah 1: Copy .env.example menjadi .env

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### Langkah 2: Edit .env dengan credentials Anda

Buka file `.env` dengan text editor dan isi:

```bash
# ============================================================
# MetaTrader 5 Account
# ============================================================
MT5_LOGIN=12345678              # Dari MT5 demo account
MT5_PASSWORD=YourPassword123    # Password MT5
MT5_SERVER=BrokerName-Demo      # Server name dari MT5
MT5_PATH=                       # Kosongkan (auto-detect)

# ============================================================
# Telegram API
# ============================================================
TELEGRAM_API_ID=12345678        # Dari my.telegram.org
TELEGRAM_API_HASH=abcdef123...  # Dari my.telegram.org
TELEGRAM_PHONE=+628123456789    # Nomor HP Telegram Anda

# ============================================================
# Trading Configuration
# ============================================================
DEFAULT_LOT_SIZE=0.01           # Micro lot (safe untuk testing)
STOP_LOSS_PERCENT=1.0           # SL 1%
TAKE_PROFIT_PERCENT=10.0        # TP 10%
CHECK_INTERVAL=60               # Check setiap 60 detik

# ============================================================
# Risk Management
# ============================================================
MAX_DAILY_LOSS=50.0             # Stop jika loss $50/day
MAX_DAILY_PROFIT=200.0          # Lock profit jika profit $200/day
MAX_TRADES_PER_DAY=20           # Max 20 trades per hari
MAX_CONSECUTIVE_LOSSES=3        # Stop setelah 3 loss berturut

# ============================================================
# Environment
# ============================================================
ENVIRONMENT=demo                # ALWAYS use demo first!
```

### Langkah 3: Verify .env

Buat file `test_env.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

print("🔍 Checking .env configuration...")
print(f"MT5_LOGIN: {os.getenv('MT5_LOGIN')}")
print(f"MT5_SERVER: {os.getenv('MT5_SERVER')}")
print(f"TELEGRAM_API_ID: {os.getenv('TELEGRAM_API_ID')}")
print(f"TELEGRAM_PHONE: {os.getenv('TELEGRAM_PHONE')}")
print(f"DEFAULT_LOT_SIZE: {os.getenv('DEFAULT_LOT_SIZE')}")

if all([
    os.getenv('MT5_LOGIN'),
    os.getenv('MT5_PASSWORD'),
    os.getenv('MT5_SERVER'),
    os.getenv('TELEGRAM_API_ID'),
    os.getenv('TELEGRAM_API_HASH'),
    os.getenv('TELEGRAM_PHONE')
]):
    print("\n✅ All credentials found!")
else:
    print("\n❌ Some credentials missing!")
```

Jalankan:
```bash
python test_env.py
```

---

## 🚀 Menjalankan Bot

### Pre-Flight Checklist:

✅ MT5 Terminal sedang running  
✅ Sudah login ke akun demo  
✅ File `.env` sudah diisi dengan benar  
✅ Dependencies sudah terinstall  
✅ Telegram session sudah terkoneksi  

### Jalankan Bot:

```bash
python forex_ai_bot.py
```

### Output yang Diharapkan:

```
╔═══════════════════════════════════════════════════════════════════╗
║     FOREX AI BOT - MULTI-PAIR TELEGRAM NEWS TRADING              ║
╚═══════════════════════════════════════════════════════════════════╝

✅ MT5 initialized
✅ Logged in to MT5 account: 12345678
   Server: BrokerName-Demo
   Balance: $10000.00
   Equity: $10000.00
   Leverage: 1:500
   ✅ DEMO ACCOUNT (Safe for testing)

✅ Found 28 tradable forex pairs
✅ Connected to Telegram

======================================================================
🤖 MULTI-PAIR FOREX AI BOT STARTED
======================================================================
Available Pairs: 28
Default Lot Size: 0.01
Stop Loss: 1.0%
Take Profit: 10.0%
Check Interval: 60s
Max Daily Trades: 20
Max Daily Loss: $50.0
Max Daily Profit: $200.0
======================================================================

⏰ 2024-02-09 10:15:30

📊 Monitoring 0 open position(s)...

📱 Fetching news from Telegram channels...
   Found 3 new message(s)

📰 New message from @marketfeed:
   BREAKING: EUR surges on positive ECB economic outlook...
   📊 Sentiment: LONG (Score: 0.685, Strength: strong)
   🎯 Affected currencies: EUR, USD
   💹 Trading pairs: EURUSD, EURJPY, EURGBP, GBPUSD, USDJPY

======================================================================
✅ LONG ORDER OPENED - EURUSD
======================================================================
Entry Price: 1.08450
Stop Loss: 1.07366 (-1.0%)
Take Profit: 1.19295 (+10.0%)
Volume: 0.01
Sentiment Score: 0.685
Signal Strength: strong
Order ID: 123456789
Daily Trades: 1/20
======================================================================

💤 Waiting 60 seconds for next check...
```

### Stop Bot:

Tekan `Ctrl + C` untuk stop bot dengan aman.

---

## 🔧 Troubleshooting

### Problem 1: "MT5 initialization failed"

**Solusi:**
1. Pastikan MT5 Terminal sudah running
2. Pastikan sudah login ke akun
3. Restart MT5 Terminal
4. Coba jalankan bot lagi

### Problem 2: "MT5 login failed"

**Solusi:**
1. Check MT5_LOGIN, MT5_PASSWORD, MT5_SERVER di `.env`
2. Pastikan tidak ada spasi atau typo
3. Login manual dulu di MT5 Terminal
4. Jika berhasil manual, credentials Anda benar

### Problem 3: "Telegram credentials not found"

**Solusi:**
1. Check file `.env` ada dan terisi
2. Pastikan TELEGRAM_API_ID adalah angka (tanpa quotes)
3. Pastikan TELEGRAM_API_HASH dalam quotes
4. Format nomor HP: +628123456789 (dengan +)

### Problem 4: "Symbol not found" atau "Pair not found"

**Solusi:**
1. Check nama pair di MT5 Market Watch
2. Nama mungkin beda: `EURUSD` vs `EURUSDm` vs `EURUSD.`
3. Klik kanan di Market Watch → Show All
4. Pair harus visible untuk bisa ditrade

### Problem 5: "Order failed" / "Invalid stops"

**Solusi:**
1. Check market hours (market harus buka)
2. Reduce lot size (coba 0.01)
3. Widen SL/TP (coba SL 2%, TP 5%)
4. Check margin (pastikan cukup balance)

### Problem 6: Bot tidak dapat news dari Telegram

**Solusi:**
1. Check koneksi internet
2. Pastikan Anda sudah join channel @marketfeed dan @wfwitness
3. Run `test_telegram.py` untuk verify
4. Check file `forex_bot_session.session` ada
5. Delete session file dan login ulang jika perlu

### Problem 7: "Too many requests" dari Telegram

**Solusi:**
1. Increase CHECK_INTERVAL di `.env` (contoh: 120 detik)
2. Telegram punya rate limit
3. Bot akan auto-retry setelah beberapa saat

---

## 📊 Monitoring & Logs

### File yang Dibuat Bot:

1. **forex_bot_session.session**
   - Telegram login session
   - Jangan dihapus kecuali mau login ulang

2. **trading_log.json** (jika ada)
   - History semua trades
   - Untuk analisis performance

### Monitor Performance:

Bot akan print real-time:
- 📊 Open positions
- 💰 Total floating P/L
- 📱 New messages from Telegram
- 📊 Sentiment analysis
- ✅ Orders opened/closed
- ⚠️ Risk limit warnings

---

## 🎯 Tips & Best Practices

### 1. ALWAYS Start with Demo
- Jangan langsung ke akun real
- Test minimal 1-2 minggu di demo
- Understand bot behavior dulu

### 2. Start Small
- Use 0.01 lot size
- Set conservative limits
- Gradually increase jika profitable

### 3. Monitor Regularly
- Check bot setiap beberapa jam
- Watch for errors atau unusual behavior
- Keep MT5 Terminal open

### 4. Risk Management
- Never risk more than 1-2% per trade
- Set daily loss limit
- Don't be greedy dengan daily profit target

### 5. News Quality
- Not all news sama pentingnya
- Bot akan filter based on sentiment strength
- Moderate/Strong/Very Strong signals only

### 6. Keep Updated
- Update MT5 Terminal regularly
- Update Python packages: `pip install -r requirements.txt --upgrade`
- Check Telegram channels masih aktif

---

## 🆘 Support

### Jika Ada Masalah:

1. **Check error message** dengan teliti
2. **Read Troubleshooting** section
3. **Test components** satu-satu:
   - `test_mt5.py`
   - `test_telegram.py`
   - `test_env.py`

4. **Common fixes:**
   - Restart MT5
   - Restart bot
   - Delete session file
   - Re-check .env

---

## ⚠️ DISCLAIMER

**PENTING - BACA DENGAN TELITI:**

1. **Trading Risk:**
   - Forex trading sangat berisiko
   - Bisa kehilangan seluruh modal
   - Past performance ≠ future results

2. **Bot Limitations:**
   - Bot BUKAN jaminan profit
   - AI bisa salah analisis
   - News bisa misleading

3. **Tanggung Jawab:**
   - Anda 100% bertanggung jawab atas trades Anda
   - Creator tidak bertanggung jawab atas losses
   - ALWAYS trade responsibly

4. **Recommendation:**
   - Use DEMO account untuk learning
   - Start with SMALL lot sizes
   - NEVER trade money you can't afford to lose

---

**Good luck with your trading! 🚀**

**Remember: The best trader is a DISCIPLINED trader! 🎯**
