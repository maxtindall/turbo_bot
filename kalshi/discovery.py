import requests
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from config import BASE_URL, KALSHI_API_KEY

HEADERS = {"Authorization": f"Bearer {KALSHI_API_KEY}"}

# Confirmed Philadelphia weather series tickers from Kalshi /series endpoint
WEATHER_SERIES = [
    "KXHIGHPHIL",   # Highest temperature in Philadelphia
    "KXPHILHIGH",   # Highest temperature in Philadelphia (alt series)
    "KXLOWPHIL",    # Lowest temperature in Philadelphia
    "KXLOWTPHIL",   # Lowest temperature in Philadelphia (alt series)
]

PHL_KEYWORDS = ["phl", "philadelphia", "philly"]


def fetch_series_markets(series_ticker):
    """Fetch all open markets for a given series ticker."""
    markets = []
    cursor = None

    while True:
        params = {"limit": 100, "status": "open", "series_ticker": series_ticker}
        if cursor:
            params["cursor"] = cursor

        try:
            res = requests.get(f"{BASE_URL}/markets", headers=HEADERS, params=params, timeout=10)
            if res.status_code != 200:
                break
            data = res.json()
            batch = data.get("markets", [])
            if not batch:
                break
            markets.extend(batch)
            cursor = data.get("cursor")
            if not cursor:
                break
        except Exception as e:
            print(f"Error fetching series {series_ticker}: {e}")
            break

    return markets


def fetch_events(series_ticker):
    """Fetch events for a given series ticker, then get their markets."""
    markets = []
    try:
        res = requests.get(
            f"{BASE_URL}/events",
            headers=HEADERS,
            params={"limit": 100, "status": "open", "series_ticker": series_ticker},
            timeout=10
        )
        if res.status_code != 200:
            return []

        events = res.json().get("events", [])
        print(f"  Found {len(events)} events for series {series_ticker}")

        for event in events:
            event_ticker = event.get("event_ticker", "")
            # Get markets for this event
            r2 = requests.get(
                f"{BASE_URL}/markets",
                headers=HEADERS,
                params={"limit": 100, "event_ticker": event_ticker, "status": "open"},
                timeout=10
            )
            if r2.status_code == 200:
                markets.extend(r2.json().get("markets", []))

    except Exception as e:
        print(f"Error fetching events for {series_ticker}: {e}")

    return markets


def normalize_market(m):
    return {
        "ticker": m.get("ticker") or m.get("market_ticker") or "",
        "title": (m.get("title") or m.get("subtitle") or m.get("yes_sub_title") or "").strip(),
        "event_ticker": (m.get("event_ticker") or "").strip(),
        "series_ticker": (m.get("series_ticker") or "").strip(),
        "raw": m
    }


def is_phl_weather_market(m):
    combined = (m["title"] + " " + m["event_ticker"] + " " + m["ticker"] + " " + m["series_ticker"]).lower()
    return any(kw in combined for kw in PHL_KEYWORDS)


def get_phl_markets():
    print("\nSEARCHING FOR PHILADELPHIA WEATHER MARKETS...")
    all_markets = []

    for series in WEATHER_SERIES:
        print(f"\nProbing series: {series}")

        # Try events endpoint first
        batch = fetch_events(series)
        if batch:
            print(f"  Got {len(batch)} markets via events")
            all_markets.extend(batch)
            continue

        # Fall back to direct series filter
        batch = fetch_series_markets(series)
        if batch:
            print(f"  Got {len(batch)} markets via series filter")
            all_markets.extend(batch)

    if not all_markets:
        print("\nNo weather series markets found.")
        print("Tip: run debug_series.py to discover active weather series tickers.")
        return []

    print(f"\nTotal weather markets found: {len(all_markets)}")

    markets = [normalize_market(m) for m in all_markets]
    filtered = [m for m in markets if is_phl_weather_market(m)]

    print(f"Philadelphia weather markets: {len(filtered)}")
    for m in filtered:
        print(f"  {m['ticker']} | {m['title']}")

    return filtered
