"""
Probe the Kalshi /series and /events endpoints to find weather market series tickers.
Run this once to discover the correct series names, then update WEATHER_SERIES in discovery.py.
"""
import requests
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("KALSHI_API_KEY", "")
BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("=== PROBING /series ===")
try:
    res = requests.get(f"{BASE_URL}/series", headers=HEADERS, timeout=10)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        series_list = res.json().get("series", [])
        print(f"Total series: {len(series_list)}")
        for s in series_list:
            ticker = s.get("ticker", "")
            title = s.get("title", "")
            if any(w in (ticker + title).lower() for w in ["temp", "weather", "rain", "high", "low", "wind"]):
                print(f"  WEATHER: {ticker} | {title}")
    else:
        print(f"Response: {res.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")

print("\n=== PROBING /events (weather keywords) ===")
for keyword in ["temp", "weather", "high", "philadelphia"]:
    try:
        res = requests.get(
            f"{BASE_URL}/events",
            headers=HEADERS,
            params={"limit": 100, "status": "open"},
            timeout=10
        )
        if res.status_code == 200:
            events = res.json().get("events", [])
            matches = [e for e in events if keyword in (e.get("title", "") + e.get("event_ticker", "")).lower()]
            if matches:
                print(f"\nKeyword '{keyword}': {len(matches)} matches")
                for e in matches[:5]:
                    print(f"  {e.get('event_ticker')} | {e.get('series_ticker')} | {e.get('title')}")
    except Exception as ex:
        print(f"Exception for '{keyword}': {ex}")
