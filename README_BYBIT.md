# 🤖 Bybit Futures AI Trading Bot (BETA)

> **Bot trading masa depan berbasis AI (Google Gemini) yang dioptimalkan untuk Bybit Futures.**  
> Menggunakan strategi "Fee-Aware Dynamic Leverage" untuk memaksimalkan ROI dan meminimalisir biaya admin bursa.

---

## ✨ Fitur Unggulan (Versi Bybit)

- 📈 **Dynamic Leverage (2x - 10x)** — Leverage diatur otomatis oleh AI berdasarkan volatilitas pasar dan tingkat keyakinan (*Confidence*).
- 💰 **Unified Trading Account (UTA) Support** — Mendukung penarikan saldo dari akun terpadu Bybit secara otomatis.
- 🛡️ **Isolated Margin Guard** — Memastikan bot selalu menggunakan mode *Isolated* untuk melindungi sisa saldo Anda.
- ⚖️ **Fee-Aware ROI Projection** — Bot menghitung proyeksi keuntungan bersih (setelah dikurangi fee Taker & Funding) sebelum mengeksekusi trade.
- 🧠 **AI-Driven Sizing (20% - 50%)** — Alokasi modal dinamis untuk mencegah "All-in" yang berisiko.
- 📰 **News Manager 2.0** — Sistem pengambilan berita yang lebih stabil dengan proteksi kegagalan API.

---

## 📋 Persyaratan Sistem

| Kebutuhan | Keterangan |
|-----------|-----------|
| OS | Ubuntu / Debian / Pop!_OS (Linux) |
| Python | 3.12 (Direkomendasikan) |
| RAM | Minimal 2GB |
| Akun | Bybit Unified Trading Account (UTA) |

---

## 🚀 Panduan Instalasi (Server Baru)

### 1. Persiapan Lingkungan
```bash
git clone <URL_REPO_ANDA>
cd <NAMA_FOLDER>
chmod +x install.sh
./install.sh
```

### 2. Konfigurasi API Keys
Edit file `keys.env` di root folder:
```env
BYBIT_API_KEY=your_key_here
BYBIT_API_SECRET=your_secret_here
GOOGLE_STUDIO_API_KEY=your_gemini_key
CRYPTOCOMPARE_API_KEY=optional_news_key
```

### 3. Pengaturan Bybit (config/config.ini)
Pastikan bagian ini sesuai:
```ini
[exchanges]
supported = bybit
sandbox_mode = false  # Ubah ke true untuk simulasi/testnet

[general]
crypto_pair = BTC/USDT:USDT
timeframe = 15m
```

---

## ⚡ Cara Menjalankan

### Mode Standar:
```bash
./run.sh
```

### Mode Latar Belakang (Rekomendasi):
Gunakan `tmux` agar bot tetap jalan saat Anda logout:
```bash
tmux new -s trading_bot
./run.sh
# Tekan Ctrl+B lalu D untuk keluar (detach)
```

Untuk masuk kembali:
```bash
tmux attach -t trading_bot
```

---

## 📊 Monitoring
- **Dashboard**: Akses `http://localhost:8000` di browser.
- **Log Real-time**: `tail -f logs/Bot/$(date +%Y_%m_%d)/Bot.log`

---

## ⚠️ Disclaimer
Trading Futures melibatkan risiko tinggi dan leverage dapat mempercepat kerugian. Bot ini adalah alat bantu analisa, gunakan modal yang siap Anda tanggung kerugiannya (Risk Capital).

---
Made with ❤️ for Bybit Traders
