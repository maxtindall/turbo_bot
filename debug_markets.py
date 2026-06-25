"""
Debug script: dumps all market titles from both Kalshi API endpoints.
Run this to figure out which URL has weather markets and what their titles look like.
"""
import requests
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("KALSHI_API_KEY", "")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

URLS = [
    "https://trading-api.kalshi.com/trade-api/v2",
    "https://api.elections.kalshi.com/trade-api/v2",
]

SEARCH_TERMS = ["weather", "temp", "rain", "wind", "snow", "philadelphia", "phl", "high", "forecast"]

for base in URLS:
    print(f"\n{'='*60}")
    print(f"TRYING: {base}")
    print('='*60)

    try:
        res = requests.get(
            f"{base}/markets",
            headers=HEADERS,
            params={"limit": 200, "status": "open"},
            timeout=10
        )
        print(f"STATUS: {res.status_code}")

        if res.status_code != 200:
            print(f"FAILED: {res.text[:300]}")
            continue

        data = res.json()
        markets = data.get("markets", [])
        print(f"TOTAL MARKETS RETURNED: {len(markets)}\n")

        print("--- ALL MARKET TITLES (first 50) ---")
        for m in markets[:50]:
            title = m.get("title") or m.get("event_title") or m.get("name") or ""
            ticker = m.get("ticker") or m.get("market_ticker") or ""
            event = m.get("event_ticker") or ""
            print(f"  {ticker:40} | {event:30} | {title}")

        print("\n--- WEATHER-RELATED MARKETS ---")
        found = 0
        for m in markets:
            title = (m.get("title") or m.get("event_title") or m.get("name") or "").lower()
            if any(t in title for t in SEARCH_TERMS):
                ticker = m.get("ticker") or m.get("market_ticker") or ""
                event = m.get("event_ticker") or ""
                print(f"  {ticker:40} | {event:30} | {title}")
                found += 1
        if not found:
            print("  (none found)")

    except Exception as e:
        print(f"EXCEPTION: {e}")
