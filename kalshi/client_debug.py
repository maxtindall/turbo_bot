import requests
import json
from config import BASE_URL, KALSHI_API_KEY

HEADERS = {
    "Authorization": f"Bearer {KALSHI_API_KEY}"
}


def fetch_markets(limit=50, max_pages=5):
    print("🚨 ENTERING fetch_markets")

    all_markets = []
    cursor = None
    page = 0

    while page < max_pages:
        print(f"\n📄 PAGE {page}")

        params = {
            "limit": limit,
            "status": "open"
        }

        if cursor:
            params["cursor"] = cursor

        try:
            print("➡️ Sending request to:", f"{BASE_URL}/markets")

            res = requests.get(
                f"{BASE_URL}/markets",
                headers=HEADERS,
                params=params,
                timeout=5
            )

            print("⬅️ Response received")
            print("STATUS:", res.status_code)
            print("RAW TEXT PREVIEW:", res.text[:200])

        except Exception as e:
            print("❌ REQUEST FAILED HARD:", e)
            return []

        try:
            data = res.json()
        except Exception as e:
            print("❌ JSON PARSE ERROR:", e)
            print("RAW:", res.text[:500])
            return []

        # --- DEBUG STRUCTURE ---
        print("\n🔑 TOP LEVEL KEYS:", list(data.keys()))

        if "data" in data:
            print("🔑 DATA KEYS:", list(data["data"].keys()))

        print("\n📦 SAMPLE RESPONSE:")
        print(json.dumps(data, indent=2)[:1000])

        # --- SAFE EXTRACTION ---
        markets = extract_markets(data)
        print(f"\n📊 MARKETS IN PAGE {page}: {len(markets)}")

        if not markets:
            print("⚠️ No markets extracted from this page")
            break

        all_markets.extend(markets)

        cursor = data.get("data", {}).get("cursor")
        if not cursor:
            print("🔚 No more pages")
            break

        page += 1

    print(f"\n✅ TOTAL MARKETS COLLECTED: {len(all_markets)}")
    return all_markets


def extract_markets(data):
    try:
        if "data" in data:
            d = data["data"]

            if "markets" in d:
                print("✅ Using data['markets']")
                return d["markets"]

            if "event_markets" in d:
                print("✅ Using data['event_markets']")
                return d["event_markets"]

            if "contracts" in d:
                print("✅ Using data['contracts']")
                return d["contracts"]

        if "markets" in data:
            print("✅ Using top-level 'markets'")
            return data["markets"]

    except Exception as e:
        print("❌ EXTRACTION ERROR:", e)

    print("❌ UNKNOWN RESPONSE STRUCTURE")
    return []
