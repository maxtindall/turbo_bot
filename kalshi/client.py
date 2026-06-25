import json
import requests
from config import BASE_URL, KALSHI_API_KEY

HEADERS = {
    "Authorization": f"Bearer {KALSHI_API_KEY}"
}


def _request(params):
    try:
        print("USING BASE_URL:", BASE_URL)
        res = requests.get(
            f"{BASE_URL}/markets",
            headers=HEADERS,
            params=params,
            timeout=10
        )

        print(f"\n🌐 STATUS: {res.status_code}")
        print(f"📦 SIZE: {len(res.text)} bytes")

        if res.status_code != 200:
            print("❌ RESPONSE PREVIEW:", res.text[:500])
            return {}

        try:
            return res.json()
        except Exception as e:
            print("❌ JSON DECODE FAILED:", e)
            print("❌ RAW RESPONSE PREVIEW:", res.text[:500])
            return {}

    except Exception as e:
        print("❌ REQUEST FAILED:", e)
        return {}


def fetch_markets(limit=100, max_pages=5):
    all_markets = []
    cursor = None
    page = 0

    while page < max_pages:
        params = {
            "limit": limit,
            "status": "open"
        }

        if cursor:
            params["cursor"] = cursor

        data = _request(params)
        if not data:
            break

        markets = data.get("markets") or data.get("data", {}).get("markets", [])
        print(f"📊 PAGE {page}: {len(markets)} markets")

        if not markets:
            break

        all_markets.extend(markets)

        cursor = data.get("cursor") or data.get("data", {}).get("cursor")
        if not cursor:
            break

        page += 1

    print(f"\n✅ TOTAL COLLECTED: {len(all_markets)}")
    return all_markets


def fetch_weather_markets(limit=100, max_pages=5):
    return fetch_markets(limit=limit, max_pages=max_pages)