from kalshi.client import fetch_markets

WEATHER_WORDS = (
    "temperature",
    "temp",
    "forecast",
    "rain",
    "snow",
    "wind",
    "precip",
    "high",
    "low",
    "weather"
)


def normalize_market(m):
    return {
        "ticker": m.get("ticker") or m.get("market_ticker") or m.get("id") or "",
        "title": (m.get("title") or m.get("event_title") or m.get("name") or "").strip(),
        "event_ticker": (m.get("event_ticker") or "").strip(),
        "raw": m
    }


def looks_weatherish(title):
    t = title.lower()
    return any(word in t for word in WEATHER_WORDS)


def is_phl_weather_market(m):
    title = m["title"].lower()
    event = m["event_ticker"].lower()

    if "philadelphia" not in title and "phl" not in title:
        return False

    if any(x in event for x in ("sports", "crosscategory", "nba", "mlb", "nhl", "nfl", "soccer", "ufc")):
        return False

    return looks_weatherish(title)


def get_phl_markets():
    print("\n🔍 FETCHING MARKETS (broad scan)...")

    raw_markets = fetch_markets(limit=100, max_pages=10)

    if not raw_markets:
        print("❌ No markets returned from API")
        return []

    print(f"\n📊 TOTAL SCANNED: {len(raw_markets)}")

    markets = [normalize_market(m) for m in raw_markets]

    print("\n--- SAMPLE MARKETS ---")
    for m in markets[:10]:
        print(m)

    print("\n--- DETECTING WEATHER MARKETS ---")
    for m in markets[:20]:
        if looks_weatherish(m["title"]):
            print("🌤", m["title"], "|", m["event_ticker"])

    filtered = [m for m in markets if is_phl_weather_market(m)]

    print(f"\n🌤 TOTAL WEATHER MARKETS FOUND: {sum(1 for m in markets if looks_weatherish(m['title']))}")
    print(f"🎯 PHILADELPHIA WEATHER MARKETS: {len(filtered)}")

    for m in filtered:
        print("✅", m["title"])

    return filtered