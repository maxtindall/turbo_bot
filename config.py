import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ===============================
# TURBO BOT CONFIG v0.0.1 STABLE
# ===============================

# --- API CONFIG ---

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

# API key loaded from environment variable (set in .env or shell)
# Never hardcode this value here
KALSHI_API_KEY = os.environ.get("KALSHI_API_KEY", "")


# --- REQUEST SETTINGS ---

REQUEST_TIMEOUT = 10
MAX_RETRIES = 3


# --- MARKET SETTINGS ---

# Pagination tuning
DEFAULT_LIMIT = 100
MAX_PAGES = 10


# --- STRATEGY SETTINGS ---

# Minimum edge required to trade
EDGE_THRESHOLD = 0.05

# Trade size (contracts)
TRADE_SIZE = 10


# --- DEBUG SETTINGS ---

DEBUG = True
PRINT_RESPONSE_SIZE = True
PRINT_SAMPLE_MARKETS = True


# --- SAFETY FLAGS ---

# Set to False to disable real trading
LIVE_TRADING = False

# Prevents accidental overtrading
MAX_TRADES_PER_RUN = 5

# --- EXECUTION SETTINGS (REQUIRED FOR ENGINE) ---

# True = no real trades (safe mode)
# False = live trading
DRY_RUN = True

# SQLite database path for tracking trades
DB_PATH = "trades.db"

# --- FUTURE SWITCH (IMPORTANT) ---

# When your account gets access to full exchange:
# Change ONLY this line:
#
# BASE_URL = "https://trading-api.kalshi.com/v1"
#
# Everything else will continue working
