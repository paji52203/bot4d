module.exports = {
  apps: [{
    name: "bybit-bot",
    script: "start.py",
    interpreter: "/root/bot_bybit/.venv/bin/python",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "2G",
    env: {
      PYTHONUNBUFFERED: "1",
      QT_QPA_PLATFORM: "offscreen"
    },
    error_file: "/root/bot_bybit/logs/pm2_error.log",
    out_file: "/root/bot_bybit/logs/pm2.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    merge_logs: true
  }]
};
