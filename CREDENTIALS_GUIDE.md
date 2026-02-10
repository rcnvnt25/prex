# 📝 CARA MENDAPATKAN SEMUA CREDENTIALS

Guide lengkap step-by-step untuk mendapatkan semua credentials yang dibutuhkan bot.

---

## 1️⃣ TELEGRAM API CREDENTIALS

### Yang Dibutuhkan:
- ✅ TELEGRAM_API_ID (angka)
- ✅ TELEGRAM_API_HASH (string panjang)
- ✅ TELEGRAM_PHONE (nomor HP)

### Cara Mendapatkan:

#### Step 1: Buka Browser
URL: **https://my.telegram.org/auth**

```
┌──────────────────────────────────────────┐
│  Telegram                                │
│  ════════════════════════════════════    │
│                                          │
│  Login to Telegram                       │
│                                          │
│  Phone number:                           │
│  ┌────────────────────────────────────┐  │
│  │ +62 812 3456 789                   │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Country: Indonesia (auto-detect)        │
│                                          │
│  [ Keep me signed in ]                   │
│                                          │
│           [      Next      ]             │
│                                          │
└──────────────────────────────────────────┘
```

**Input:** Nomor HP yang terdaftar di Telegram
**Format:** +62812... (dengan kode negara)

#### Step 2: Masukkan Kode Verifikasi

```
┌──────────────────────────────────────────┐
│  Telegram                                │
│  ════════════════════════════════════    │
│                                          │
│  We've sent a code to your phone        │
│  +62 812 3456 789                        │
│                                          │
│  Code:                                   │
│  ┌────────────────────────────────────┐  │
│  │ 12345                              │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Didn't receive the code?                │
│  [ Resend code ]                         │
│                                          │
│           [      Next      ]             │
│                                          │
└──────────────────────────────────────────┘
```

**Check Telegram app** di HP Anda untuk kode!

#### Step 3: API Development Tools

Setelah login, pilih menu **"API development tools"**

```
┌──────────────────────────────────────────┐
│  Telegram API Development                │
│  ════════════════════════════════════    │
│                                          │
│  Your apps                               │
│  ────────────────                        │
│                                          │
│  You don't have any apps yet.            │
│                                          │
│  [ Create new application ]              │
│                                          │
└──────────────────────────────────────────┘
```

#### Step 4: Buat Application

```
┌──────────────────────────────────────────┐
│  Create new application                  │
│  ════════════════════════════════════    │
│                                          │
│  App title:                              │
│  ┌────────────────────────────────────┐  │
│  │ Forex AI Bot                       │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Short name:                             │
│  ┌────────────────────────────────────┐  │
│  │ forexbot                           │  │
│  └────────────────────────────────────┘  │
│                                          │
│  URL (optional):                         │
│  ┌────────────────────────────────────┐  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Platform:                               │
│  ( ) Android  ( ) iOS  (•) Other        │
│                                          │
│  Description (optional):                 │
│  ┌────────────────────────────────────┐  │
│  │ Forex trading bot                  │  │
│  └────────────────────────────────────┘  │
│                                          │
│         [ Create application ]           │
│                                          │
└──────────────────────────────────────────┘
```

**Fill in:**
- App title: `Forex AI Bot` (atau nama bebas)
- Short name: `forexbot` (harus unik)
- Platform: Pilih **Other**
- Description: Opsional

#### Step 5: COPY CREDENTIALS! ⭐

```
┌──────────────────────────────────────────┐
│  Application configuration               │
│  ════════════════════════════════════    │
│                                          │
│  ✅ Your application created!            │
│                                          │
│  App api_id:                             │
│  ┌────────────────────────────────────┐  │
│  │  12345678                          │  │ ← COPY INI!
│  └────────────────────────────────────┘  │
│                                          │
│  App api_hash:                           │
│  ┌────────────────────────────────────┐  │
│  │  abcdef1234567890abcdef1234567890  │  │ ← COPY INI!
│  └────────────────────────────────────┘  │
│                                          │
│  ⚠️ IMPORTANT: Save these credentials!   │
│  You'll need them to configure your bot. │
│                                          │
└──────────────────────────────────────────┘
```

**CATAT DI NOTEPAD:**
```
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_PHONE=+628123456789
```

---

## 2️⃣ METATRADER 5 CREDENTIALS

### Yang Dibutuhkan:
- ✅ MT5_LOGIN (nomor akun)
- ✅ MT5_PASSWORD (password akun)
- ✅ MT5_SERVER (nama server broker)

### Cara Mendapatkan:

#### Option A: Buat Akun Demo Baru

**Step 1: Install MT5**
- Download dari broker Anda atau dari https://www.metatrader5.com/en/download
- Install seperti biasa

**Step 2: Buka MT5 Terminal**

```
┌──────────────────────────────────────────┐
│  MetaTrader 5                       [X]  │
│  ═══════════════════════════════════     │
│  File  View  Insert  Charts  Tools       │
│  ────────────────────────────────────    │
│                                          │
│  Welcome to MetaTrader 5!                │
│                                          │
│  Get started by opening an account       │
│                                          │
│         [ Open an account ]              │
│                                          │
└──────────────────────────────────────────┘
```

**Step 3: Pilih Broker**

```
┌──────────────────────────────────────────┐
│  Open an Account                         │
│  ════════════════════════════════════    │
│                                          │
│  Search for your broker:                 │
│  ┌────────────────────────────────────┐  │
│  │ IC Markets                         │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Available servers:                      │
│  ┌────────────────────────────────────┐  │
│  │ ▸ IC Markets                       │  │
│  │   • ICMarkets-Demo                 │  │ ← Pilih Demo!
│  │   • ICMarkets-Live01               │  │
│  │   • ICMarkets-Live02               │  │
│  └────────────────────────────────────┘  │
│                                          │
│              [ Next ]                    │
│                                          │
└──────────────────────────────────────────┘
```

**Step 4: Pilih "Open a demo account"**

```
┌──────────────────────────────────────────┐
│  Account Type                            │
│  ════════════════════════════════════    │
│                                          │
│  (•) Open a demo account                 │ ← Pilih ini!
│  ( ) Open a live account                 │
│                                          │
│              [ Next ]                    │
│                                          │
└──────────────────────────────────────────┘
```

**Step 5: Isi Form Registrasi**

```
┌──────────────────────────────────────────┐
│  Demo Account Registration               │
│  ════════════════════════════════════    │
│                                          │
│  Name:                                   │
│  ┌────────────────────────────────────┐  │
│  │ Your Name                          │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Email:                                  │
│  ┌────────────────────────────────────┐  │
│  │ your@email.com                     │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Phone:                                  │
│  ┌────────────────────────────────────┐  │
│  │ +62812345678                       │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Account type:                           │
│  [ Standard v ] (pilih yang low spread)  │
│                                          │
│  Deposit:                                │
│  [ 10000 v ] USD                         │
│                                          │
│  Leverage:                               │
│  [ 1:500 v ]                             │
│                                          │
│  Currency:                               │
│  [ USD v ]                               │
│                                          │
│  [ I agree to terms and conditions ]     │
│                                          │
│              [ Next ]                    │
│                                          │
└──────────────────────────────────────────┘
```

**Recommendations:**
- Account type: Standard / Raw Spread / ECN
- Deposit: $10,000 (cukup untuk testing)
- Leverage: 1:500 (standard)
- Currency: USD

**Step 6: ✅ CREDENTIALS CREATED!**

```
┌──────────────────────────────────────────┐
│  Registration Successful!                │
│  ════════════════════════════════════    │
│                                          │
│  Your demo account has been created:     │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Login:    12345678               │  │ ← CATAT!
│  │  Password: abcd1234               │  │ ← CATAT!
│  │  Server:   ICMarkets-Demo         │  │ ← CATAT!
│  └────────────────────────────────────┘  │
│                                          │
│  ⚠️ SAVE THESE CREDENTIALS!              │
│                                          │
│  An email with these details has been    │
│  sent to your@email.com                  │
│                                          │
│              [ Finish ]                  │
│                                          │
└──────────────────────────────────────────┘
```

**CATAT DI NOTEPAD:**
```
MT5_LOGIN=12345678
MT5_PASSWORD=abcd1234
MT5_SERVER=ICMarkets-Demo
```

#### Option B: Gunakan Akun yang Sudah Ada

Jika sudah punya akun MT5:

**Step 1: Buka MT5**

**Step 2: File → Login to Trade Account**

**Step 3: Lihat Credentials:**

```
┌──────────────────────────────────────────┐
│  Login                                   │
│  ════════════════════════════════════    │
│                                          │
│  Login:                                  │
│  ┌────────────────────────────────────┐  │
│  │ 12345678                           │  │ ← Login number
│  └────────────────────────────────────┘  │
│                                          │
│  Password:                               │
│  ┌────────────────────────────────────┐  │
│  │ ••••••••                           │  │ ← Password Anda
│  └────────────────────────────────────┘  │
│                                          │
│  Server:                                 │
│  [ ICMarkets-Demo          v ]           │ ← Server name
│                                          │
│  [ Save password ]                       │
│                                          │
│              [ Login ]                   │
│                                          │
└──────────────────────────────────────────┘
```

**Check juga di email** broker biasanya kirim credentials.

---

## 3️⃣ MASUKKAN KE FILE .env

Setelah dapat semua credentials, buat file `.env`:

### Windows:
```cmd
copy .env.example .env
notepad .env
```

### Linux/Mac:
```bash
cp .env.example .env
nano .env
```

### ISI FILE .env:

```bash
# ============================================================
# MetaTrader 5 Account Configuration
# ============================================================
MT5_LOGIN=12345678                    # ← Ganti dengan Login Anda
MT5_PASSWORD=abcd1234                 # ← Ganti dengan Password Anda
MT5_SERVER=ICMarkets-Demo             # ← Ganti dengan Server Anda
MT5_PATH=                             # ← Kosongkan (auto-detect)

# ============================================================
# Telegram API Configuration
# ============================================================
TELEGRAM_API_ID=12345678              # ← Ganti dengan api_id Anda
TELEGRAM_API_HASH=abcdef1234567890... # ← Ganti dengan api_hash Anda
TELEGRAM_PHONE=+628123456789          # ← Ganti dengan nomor HP Anda

# ============================================================
# Trading Configuration (BISA DIUBAH NANTI)
# ============================================================
DEFAULT_LOT_SIZE=0.01
STOP_LOSS_PERCENT=1.0
TAKE_PROFIT_PERCENT=10.0
CHECK_INTERVAL=60

# ============================================================
# Risk Management (BISA DIUBAH NANTI)
# ============================================================
MAX_DAILY_LOSS=50.0
MAX_DAILY_PROFIT=200.0
MAX_TRADES_PER_DAY=20
MAX_CONSECUTIVE_LOSSES=3

# ============================================================
# Environment
# ============================================================
ENVIRONMENT=demo
```

**SAVE** file ini!

---

## 4️⃣ VERIFY SETUP

### Test MT5 Connection:

Buat file `test_mt5.py`:
```python
import MetaTrader5 as mt5
from dotenv import load_dotenv
import os

load_dotenv()

login = int(os.getenv('MT5_LOGIN'))
password = os.getenv('MT5_PASSWORD')
server = os.getenv('MT5_SERVER')

if not mt5.initialize():
    print("❌ MT5 init failed")
    quit()

print("✅ MT5 initialized")

if mt5.login(login, password, server):
    print(f"✅ Logged in to {server}")
    account_info = mt5.account_info()
    print(f"   Balance: ${account_info.balance}")
else:
    print("❌ Login failed")

mt5.shutdown()
```

Run:
```bash
python test_mt5.py
```

Expected output:
```
✅ MT5 initialized
✅ Logged in to ICMarkets-Demo
   Balance: $10000.0
```

### Test Telegram Connection:

Buat file `test_telegram.py`:
```python
from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

async def main():
    client = TelegramClient('test_session', api_id, api_hash)
    await client.start(phone=phone)
    print("✅ Connected to Telegram!")
    
    # Test read from channel
    try:
        async for message in client.iter_messages('marketfeed', limit=3):
            print(f"📰 {message.date}: {message.text[:100]}...")
        print("✅ Can read from @marketfeed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    await client.disconnect()

asyncio.run(main())
```

Run:
```bash
python test_telegram.py
```

**Pertama kali:**
```
Please enter the code you received: 12345
✅ Connected to Telegram!
📰 2024-02-09: Breaking news...
📰 2024-02-09: Market update...
✅ Can read from @marketfeed
```

---

## 5️⃣ COMMON MISTAKES

### ❌ Mistake 1: Salah Format Nomor HP

**SALAH:**
```
TELEGRAM_PHONE=08123456789          # ❌ No country code
TELEGRAM_PHONE=628123456789         # ❌ No + sign
TELEGRAM_PHONE=+62 812 345 6789     # ❌ Has spaces
```

**BENAR:**
```
TELEGRAM_PHONE=+628123456789        # ✅ Correct!
```

### ❌ Mistake 2: API ID dalam Quotes

**SALAH:**
```
TELEGRAM_API_ID="12345678"          # ❌ Don't use quotes for numbers
TELEGRAM_API_ID='12345678'          # ❌ Don't use quotes for numbers
```

**BENAR:**
```
TELEGRAM_API_ID=12345678            # ✅ No quotes!
```

### ❌ Mistake 3: Lupa Join Channel

**HARUS join channel dulu:**
- https://t.me/marketfeed
- https://t.me/wfwitness

Klik "Join" di Telegram app!

### ❌ Mistake 4: MT5 Terminal Tidak Running

Bot memerlukan MT5 **running** dan **logged in**!

```
✅ MT5 terminal open
✅ Already logged in to demo account
✅ "Allow automated trading" enabled
```

---

## 📝 SUMMARY CHECKLIST

Sebelum run bot, pastikan:

### Telegram:
- [ ] Dapat api_id dari my.telegram.org
- [ ] Dapat api_hash dari my.telegram.org
- [ ] Nomor HP format: +628123456789
- [ ] Join @marketfeed
- [ ] Join @wfwitness

### MT5:
- [ ] MT5 terminal installed
- [ ] Demo account created
- [ ] Dapat Login number
- [ ] Dapat Password
- [ ] Dapat Server name
- [ ] MT5 terminal running
- [ ] Logged in to account
- [ ] "Allow automated trading" enabled

### File:
- [ ] File .env created (dari .env.example)
- [ ] All credentials filled in .env
- [ ] No typos in credentials
- [ ] Proper formatting (no extra spaces)

### Testing:
- [ ] Run test_mt5.py → Success
- [ ] Run test_telegram.py → Success
- [ ] Both tests passed

### Ready to Go:
- [ ] All checklist items done
- [ ] Run: `python forex_ai_bot.py`
- [ ] Bot should start successfully!

---

**🎉 CONGRATULATIONS!**

Jika semua checklist ✅, Anda siap menjalankan bot!

```bash
python forex_ai_bot.py
```

**Good luck! 🚀**
