TURBO BOT v0.0.1

NEW:
- Auto installer (install.sh)
- Contract threshold parsing
- Limit order logic (spread capture)
- Position management
- Basic HTML dashboard

SETUP:
chmod +x install.sh
./install.sh

RUN:
source venv/bin/activate
python bot.py

DASHBOARD:
python dashboard/app.py
http://localhost:5000

NOTES:
- Set DRY_RUN=False for live trading
- This version introduces position tracking + smarter execution
