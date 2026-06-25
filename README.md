# turbo_bot

Automated prediction market trading bot for weather markets on the Kalshi exchange.

## Overview

turbo_bot discovers live weather prediction markets, fetches real-time meteorological data, and applies a proprietary pricing model to identify and execute trades when market prices diverge from estimated fair value. The bot runs a full loop — market discovery, data ingestion, edge calculation, and order placement — in a single execution pass.

Key features:
- Automated discovery of weather markets via the Kalshi API
- Real-time weather data integration
- Configurable dry-run mode for safe testing without live order placement
- SQLite-based trade logging with status tracking
- Liquidity filters to avoid trading in thin or mispriced markets

## Requirements

- Python 3.9+
- Kalshi trading account with API access
- Dependencies listed in `requirements.txt`

## Setup

```bash
git clone https://github.com/maxtindall/turbo_bot.git
cd turbo_bot
chmod +x install.sh
./install.sh
```

Create a `.env` file in the project root:

```
KALSHI_API_KEY=your_api_key_here
```

## Usage

Activate the virtual environment and run the bot:

```bash
source venv/bin/activate
python bot.py
```

By default the bot runs in dry-run mode (`DRY_RUN = True` in `config.py`). No real orders will be placed until this is explicitly disabled.

To launch the dashboard:

```bash
python dashboard/app.py
```

Then open `http://localhost:5000` in your browser.

## Configuration

Key settings in `config.py`:

| Setting | Description |
|---|---|
| `DRY_RUN` | `True` = simulate trades only, `False` = live trading |
| `TRADE_SIZE` | Number of contracts per order |
| `EDGE_THRESHOLD` | Minimum edge required to place a trade |
| `MAX_TRADES_PER_RUN` | Safety cap on trades per bot execution |

## License

Proprietary — Copyright © 2025 Max Tindall Inc. All rights reserved.

For licensing, collaboration, or inquiries: max@maxis.fit
