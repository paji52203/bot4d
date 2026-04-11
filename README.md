# AI Bybit Futures Trading Bot (QRAK Evolution)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Exchange](https://img.shields.io/badge/exchange-Bybit%20Futures-orange.svg)

An advanced, AI-driven trading bot specialized for **Bybit Futures (Linear Perpetual)**. This bot leverage LLM intelligence to execute trades with dynamic risk management, isolated margin protection, and real-time fee awareness.

## 🚀 Key Features (Bybit Futures focus)

- **🤖 AI Dynamic Leverage**: Automatically scales leverage (2x - 10x) based on AI confidence levels and market volatility.
- **📊 Dynamic Position Sizing**: Allocates 20% to 50% of capital dynamically per trade, optimizing risk-reward ratios.
- **🛡️ Isolated Margin Protection**: Automatically enforces Isolated Margin mode for every asset to protect your entire wallet balance.
- **💰 Fee-Aware Profitability**: AI projects net ROI after deducting Taker fees and Funding rates *before* entering a trade.
- **📈 Unified Trading Account (UTA)**: Native support for Bybit's Unified Trading Account architecture.
- **📉 ATR-Based Risk Guardrails**: Uses Average True Range (ATR) for intelligent stop-loss and take-profit placement.

## 🛠️ Installation

### 1. Requirements
- Python 3.10 or higher
- A Bybit API Key with **Futures/Contract** permissions enabled.

### 2. Clone the Repository
```bash
git clone https://github.com/USER/futures-bybit-bot-qrak.git
cd futures-bybit-bot-qrak
```

### 3. Setup Virtual Environment
```bash
chmod +x install.sh
./install.sh
```

### 4. Configuration
Create a `keys.env` file (copy from `keys.env.example`):
```bash
cp keys.env.example keys.env
```
Fill in your `BYBIT_API_KEY`, `BYBIT_API_SECRET`, and chosen `MODEL_NAME` (e.g., Gemini 2.0 Flash).

## 🚦 Usage

### Start Trading
```bash
chmod +x run.sh
./run.sh
```

### Update Bot (Safe Update)
To pull latest changes from GitHub without losing your local trade history or logs:
```bash
./update.sh
```

## 📉 Comparison with Original QRAK (Spot)

This version is a complete overhaul of the original QRAK Spot (Tokocrypto/Indodax) bot. See [COMPARISON.md](./COMPARISON.md) for a detailed technical breakdown.

| Improvement | Original (Spot) | Evolution (Futures) |
| :--- | :--- | :--- |
| **Leverage** | 1x Only | **Dynamic 2x - 10x** |
| **Market Type** | Spot Only | **Long & Short** |
| **Risk Control** | Static 30% | **Dynamic (20-50%)** |
| **Protection** | Cross Margin | **Mandatory Isolated** |

## ⚖️ Disclaimer
Trading futures involves significant risk of loss and is not suitable for all investors. Use this bot at your own risk. The authors are not responsible for any financial losses incurred.
