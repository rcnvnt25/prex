# 🤖 Forex AI Trading Bot - News Sentiment Analysis

Bot trading forex otomatis yang menggunakan AI untuk menganalisis sentimen berita dan melakukan trading berdasarkan good news atau bad news dengan manajemen risiko otomatis.

## ✨ Fitur Utama

### 1. **Analisis Sentimen Berita Otomatis**
- Menganalisis berita forex secara real-time
- Mendeteksi bullish (good news) atau bearish (bad news) sentiment
- Scoring otomatis dengan AI keyword analysis

### 2. **Trading Otomatis Berdasarkan News**
- **Good News** → Otomatis OPEN posisi BUY
- **Bad News** → Otomatis OPEN posisi SELL
- Eksekusi instant ketika ada berita dengan impact tinggi

### 3. **Risk Management Otomatis**
- **Stop Loss**: 1% dari harga entry (auto close jika minus 1%)
- **Take Profit**: 10% dari harga entry (auto close jika profit 10%)
- Proteksi modal dengan risk/reward ratio 1:10

### 4. **Integrasi Penuh dengan MT5**
- Koneksi langsung ke MetaTrader 5
- Order execution otomatis
- Real-time monitoring posisi

## 📋 Persyaratan Sistem

### Software yang Dibutuhkan:
1. **Python 3.8+** ([Download](https://www.python.org/downloads/))
2. **MetaTrader 5** ([Download](https://www.metatrader5.com/en/download))
3. **Akun Trading MT5** (Demo atau Real)

### Operating System:
- ✅ Windows 10/11 (Recommended)
- ⚠️ Linux (via Wine)
- ⚠️ macOS (via Virtual Machine atau Wine)

## 🚀 Instalasi

### Langkah 1: Clone atau Download Project
```bash
# Download semua file ke folder project Anda
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install MetaTrader5 pandas numpy requests
```

### Langkah 3: Setup MetaTrader 5

1. **Install dan Login MT5**
   - Download dan install MT5
   - Login dengan akun demo atau real Anda

2. **Enable Algo Trading**
   - Buka MT5
   - Klik Tools → Options
   - Tab "Expert Advisors"
   - ✅ Centang "Allow automated trading"
   - ✅ Centang "Allow DLL imports"

3. **Pastikan Terminal MT5 Terbuka**
   - Bot memerlukan MT5 dalam keadaan running
   - Jangan close terminal MT5 saat bot berjalan

## 🎯 Cara Menggunakan

### Konfigurasi Dasar

Edit bagian `config` di file `forex_ai_bot.py`:

```python
config = {
    'symbol': 'EURUSD',           # Pair yang akan ditrade
    'lot_size': 0.01,             # Ukuran lot (0.01 = 1 micro lot)
    'stop_loss_percent': 1.0,     # Stop loss 1%
    'take_profit_percent': 10.0,  # Take profit 10%
    'check_interval': 60          # Check setiap 60 detik
}
```

#### Penjelasan Parameter:

| Parameter | Deskripsi | Contoh |
|-----------|-----------|--------|
| `symbol` | Pair forex yang akan ditrade | `'EURUSD'`, `'GBPUSD'`, `'USDJPY'` |
| `lot_size` | Ukuran lot trading | `0.01` (micro), `0.1` (mini), `1.0` (standard) |
| `stop_loss_percent` | Stop loss dalam persen | `1.0` = 1% |
| `take_profit_percent` | Take profit dalam persen | `10.0` = 10% |
| `check_interval` | Interval pengecekan (detik) | `60` = 1 menit |

### Menjalankan Bot

```bash
python forex_ai_bot.py
```

### Output yang Akan Anda Lihat:

```
╔═══════════════════════════════════════════════════════════╗
║         FOREX AI BOT - NEWS SENTIMENT TRADING             ║
╚═══════════════════════════════════════════════════════════╝

✅ Connected to MetaTrader 5
✅ Symbol EURUSD is ready

🤖 FOREX AI BOT STARTED
Symbol: EURUSD
Lot Size: 0.01
Stop Loss: 1.0%
Take Profit: 10.0%

🔍 Fetching latest forex news...

📰 News: EUR Surges on Positive ECB Economic Outlook
   Sentiment: BUY (Score: 0.75, Strength: strong)
   🎯 Trading signal detected: BUY

============================================================
✅ BUY ORDER OPENED
============================================================
Symbol: EURUSD
Entry Price: 1.08450
Stop Loss: 1.07366 (-1.0%)
Take Profit: 1.19295 (+10.0%)
Volume: 0.01
Sentiment Score: 0.75
Signal Strength: strong
============================================================
```

## 🧠 Cara Kerja AI Sentiment Analysis

### 1. News Detection
Bot secara otomatis mengambil berita forex terbaru yang relevan dengan pair yang Anda trade.

### 2. Sentiment Analysis
Bot menganalisis berita dengan AI menggunakan keyword detection:

**Bullish Keywords (Good News):**
- surge, rally, gain, rise, increase, growth, stronger
- positive, optimistic, boost, improvement, expansion
- recovery, upbeat, soar, jump, advance

**Bearish Keywords (Bad News):**
- fall, drop, decline, decrease, weak, loss, crash
- negative, pessimistic, concern, worry, recession
- contraction, downward, plunge, tumble, slump

### 3. Signal Generation
- **Sentiment Score > 0.2** → BUY Signal
- **Sentiment Score < -0.2** → SELL Signal
- **-0.2 to 0.2** → NEUTRAL (no trading)

### 4. Trade Execution
Jika signal BUY atau SELL terdeteksi, bot otomatis:
1. Open posisi dengan lot size yang ditentukan
2. Set Stop Loss di -1% dari entry
3. Set Take Profit di +10% dari entry

### 5. Position Management
Bot akan otomatis:
- **Close posisi** jika harga menyentuh Stop Loss (-1%)
- **Close posisi** jika harga menyentuh Take Profit (+10%)
- **Monitor** posisi secara real-time

## 📊 Contoh Skenario Trading

### Skenario 1: Good News (BUY)
```
📰 Breaking News: "EUR Surges on Positive ECB Outlook"

🤖 Bot Action:
1. Analisis sentiment → Score: +0.75 (Strong Bullish)
2. Generate signal → BUY
3. Open BUY order:
   - Entry: 1.08450
   - SL: 1.07366 (-1%)
   - TP: 1.19295 (+10%)

📈 Hasil:
✅ Jika profit 10% → Auto Take Profit = +$10 (untuk $100 investment)
❌ Jika minus 1% → Auto Stop Loss = -$1 (untuk $100 investment)
```

### Skenario 2: Bad News (SELL)
```
📰 Breaking News: "USD Tumbles Amid Recession Fears"

🤖 Bot Action:
1. Analisis sentiment → Score: -0.68 (Strong Bearish)
2. Generate signal → SELL
3. Open SELL order:
   - Entry: 1.08450
   - SL: 1.09535 (+1%)
   - TP: 0.97605 (-10%)

📉 Hasil:
✅ Jika profit 10% → Auto Take Profit
❌ Jika minus 1% → Auto Stop Loss
```

## ⚙️ Kustomisasi Lanjutan

### Menggunakan Real News API

Untuk production, ganti fungsi simulasi dengan real news API:

```python
def get_forex_news(self, currency_pair: str = 'EURUSD') -> List[Dict]:
    """Menggunakan real news API"""
    
    # Contoh dengan NewsAPI
    api_key = 'YOUR_API_KEY'
    url = f'https://newsapi.org/v2/everything?q={currency_pair}&apiKey={api_key}'
    
    response = requests.get(url)
    news_data = response.json()
    
    news_items = []
    for article in news_data['articles'][:5]:  # Ambil 5 berita terbaru
        news_items.append({
            'title': article['title'],
            'content': article['description'],
            'timestamp': article['publishedAt'],
            'impact': 'high'
        })
    
    return news_items
```

### API News yang Direkomendasikan:
1. **NewsAPI** - https://newsapi.org/ (Free tier available)
2. **Alpha Vantage** - https://www.alphavantage.co/ (Free with API key)
3. **Forex Factory API** - Real-time forex news
4. **Bloomberg API** - Premium news source

### Mengubah Risk/Reward Ratio

```python
config = {
    'stop_loss_percent': 0.5,     # SL lebih ketat (0.5%)
    'take_profit_percent': 5.0,   # TP lebih konservatif (5%)
}
```

### Trading Multiple Pairs

```python
# Buat multiple bot instances
pairs = ['EURUSD', 'GBPUSD', 'USDJPY']

for pair in pairs:
    bot = ForexAIBot(symbol=pair, lot_size=0.01)
    # Run in separate threads
```

## ⚠️ Risk Warning & Disclaimer

**PENTING - BACA INI DENGAN TELITI:**

### ⚠️ Trading Forex Mengandung Risiko Tinggi

1. **Kerugian Modal**
   - Trading forex dapat mengakibatkan kerugian seluruh modal Anda
   - Jangan gunakan uang yang Anda tidak mampu kehilangan
   - Leverage dapat memperbesar keuntungan DAN kerugian

2. **Bot Bukan Jaminan Profit**
   - Bot ini adalah tools, BUKAN mesin uang
   - Past performance ≠ Future results
   - AI sentiment analysis bisa salah

3. **Gunakan Akun Demo Dulu**
   - **WAJIB** test di akun demo minimal 1-2 bulan
   - Pahami cara kerja bot sepenuhnya
   - Jangan langsung ke akun real

4. **Risk Management**
   - Gunakan lot size kecil (0.01 - 0.1)
   - Jangan all-in dalam satu trade
   - Set maximum daily loss limit

### 📝 Disclaimer

```
Bot ini disediakan "AS IS" untuk tujuan edukasi.
Creator tidak bertanggung jawab atas kerugian trading Anda.
Anda sepenuhnya bertanggung jawab atas keputusan trading Anda.
Selalu lakukan due diligence dan trade dengan bijak.
```

## 🐛 Troubleshooting

### Problem: "MT5 initialization failed"
**Solusi:**
1. Pastikan MT5 sudah terinstall dan running
2. Pastikan Anda sudah login ke akun MT5
3. Enable "Allow automated trading" di MT5 settings
4. Restart MT5 dan coba lagi

### Problem: "Symbol not found"
**Solusi:**
1. Check apakah pair tersedia di broker Anda
2. Buka Market Watch di MT5
3. Klik kanan → Symbols → cari pair Anda
4. Pastikan pair visible di Market Watch

### Problem: "Order failed"
**Solusi:**
1. Check apakah ada cukup margin
2. Periksa market hours (apakah market sedang buka?)
3. Coba reduce lot size
4. Check connection internet

### Problem: Bot tidak trade sama sekali
**Solusi:**
1. Periksa apakah ada berita yang masuk
2. Sentiment mungkin NEUTRAL (tidak cukup kuat)
3. Mungkin sudah ada posisi terbuka
4. Adjust threshold di kode jika perlu

## 📚 Resources

### Belajar Forex Trading:
- [BabyPips School of Pipsology](https://www.babypips.com/learn/forex)
- [Investopedia Forex Guide](https://www.investopedia.com/forex-trading-4427206)

### MetaTrader 5:
- [MT5 Documentation](https://www.mql5.com/en/docs)
- [Python MT5 API](https://www.mql5.com/en/docs/python_metatrader5)

### News Sources:
- [Forex Factory](https://www.forexfactory.com/)
- [Investing.com Economic Calendar](https://www.investing.com/economic-calendar/)
- [DailyFX](https://www.dailyfx.com/)

## 🤝 Contributing

Jika Anda ingin improve bot ini:
1. Test thoroughly di demo account
2. Document changes dengan jelas
3. Share improvements untuk komunitas

## 📞 Support

Jika ada pertanyaan atau issue:
1. Baca dokumentasi ini dengan lengkap
2. Check bagian Troubleshooting
3. Test di demo account dulu
4. Konsultasi dengan trader berpengalaman

## 📄 License

MIT License - Gunakan dengan bijak dan bertanggung jawab.

---

**Good luck with your trading! Trade smart, not hard! 📈**

**Remember: The best trader is a disciplined trader! 🎯**
