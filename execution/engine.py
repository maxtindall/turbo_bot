import sqlite3
import requests
from config import DRY_RUN, DB_PATH, BASE_URL, KALSHI_API_KEY, TRADE_SIZE

HEADERS = {
    "Authorization": f"Bearer {KALSHI_API_KEY}",
    "Content-Type": "application/json"
}

ORDER_URL = f"{BASE_URL}/portfolio/orders"


def log(m, side, price, status="dry_run"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            market TEXT,
            side TEXT,
            price REAL,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("INSERT INTO trades (market, side, price, status) VALUES (?, ?, ?, ?)",
              (m, side, price, status))
    conn.commit()
    conn.close()


def place(market, side, price):
    """
    Place a limit order on Kalshi.

    Args:
        market: market ticker (e.g. "KXTEMP-25JUN-T85")
        side:   "YES" or "NO"
        price:  float between 0 and 1 (e.g. 0.45 = 45 cents)
    """
    price_cents = max(1, min(99, round(price * 100)))

    if DRY_RUN:
        print(f"[DRY RUN] {side} {market} @ {price_cents}c  (size={TRADE_SIZE})")
        log(market, side, price, status="dry_run")
        return

    payload = {
        "ticker": market,
        "action": "buy",
        "side": side.lower(),
        "count": TRADE_SIZE,
        "type": "limit",
    }

    if side.upper() == "YES":
        payload["yes_price"] = price_cents
    else:
        payload["no_price"] = price_cents

    try:
        res = requests.post(ORDER_URL, headers=HEADERS, json=payload, timeout=10)
        print(f"ORDER STATUS: {res.status_code}")

        if res.status_code in (200, 201):
            data = res.json()
            order_id = data.get("order", {}).get("order_id", "unknown")
            print(f"ORDER PLACED: {side} {market} @ {price_cents}c | order_id={order_id}")
            log(market, side, price, status="placed")
        else:
            print(f"ORDER FAILED: {res.status_code} -- {res.text[:300]}")
            log(market, side, price, status=f"failed_{res.status_code}")

    except Exception as e:
        print(f"ORDER EXCEPTION: {e}")
        log(market, side, price, status="exception")
