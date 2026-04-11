#!/bin/bash

# Configuration
BOT_NAME="bybit-bot"
VENV_DIR="venv"
PYTHON_BIN="$VENV_DIR/bin/python3"
SCRIPT="start.py"

echo "🔍 Checking status of $BOT_NAME..."

# 1. Clean port 8000 if it is lingering
fuser -k 8000/tcp 2>/dev/null

# 2. Check if process exists in PM2
if pm2 show $BOT_NAME > /dev/null 2>&1; then
    echo "⚡ $BOT_NAME already exists in PM2."
    pm2 restart $BOT_NAME
else
    echo "🚀 Initializing $BOT_NAME in PM2..."
    pm2 start $SCRIPT --name $BOT_NAME --interpreter $PYTHON_BIN --cwd $(pwd)
    pm2 save
fi

echo "✅ Success! Bot is managed by PM2."
echo "----------------------------------------------------"
echo "👉 View logs:  pm2 logs $BOT_NAME"
echo "👉 Stop bot:   pm2 stop $BOT_NAME"
echo "👉 Start bot:  pm2 start $BOT_NAME"
echo "👉 Status:     pm2 status"
echo "----------------------------------------------------"
