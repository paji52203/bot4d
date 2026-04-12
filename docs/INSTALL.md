# Bot Bybit - Installation Guide

## 1) Clone Repository
```bash
git clone https://github.com/paji52203/bot4d.git
cd bot4d
```

## 2) Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Configure Environment
Edit file `.env` lalu isi kredensial berikut:
- `BYBIT_API_KEY`
- `BYBIT_API_SECRET`
- API key provider LLM
- Token Telegram/Discord (opsional)

Jika template tersedia:
```bash
cp .env.example .env
```

## 5) Run Bot
```bash
python start.py
```

## 6) Optional PM2
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 logs
```

## 7) Optional Validation
```bash
python -m py_compile src/agents/orchestrator.py
pytest -q
```

## Important Paths
- Main orchestrator: `src/agents/orchestrator.py`
- Main app loop: `src/app.py`
