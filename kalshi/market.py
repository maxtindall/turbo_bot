import requests
from config import BASE_URL, KALSHI_API_KEY

HEADERS = {"Authorization": f"Bearer {KALSHI_API_KEY}"}


def get_orderbook(mid):
    res = requests.get(
        f"{BASE_URL}/markets/{mid}/orderbook",
        headers=HEADERS,
        timeout=10
    )
    res.raise_for_status()
    return res.json()


MIN_BID   = 0.05   # ignore YES bids below this — likely noise
MAX_SPREAD = 0.30  # ignore markets where ask - bid exceeds this — too illiquid


def get_bid_ask(ob):
    """
    Extract best YES bid and YES ask from an orderbook response.

    Kalshi orderbook format:
      ob["orderbook_fp"]["yes_dollars"] = [["0.4500", "100.00"], ...]  (YES bids, highest first)
      ob["orderbook_fp"]["no_dollars"]  = [["0.5500", "100.00"], ...]  (NO bids, highest first)

    YES bid  = best YES bid price         (what buyers will pay for YES)
    YES ask  = 1 - best NO bid price      (what sellers want for YES, derived from NO side)

    Prices are already in 0-1 float range.
    Returns (bid, ask) or (None, None) if no liquidity or market fails quality filters.
    """
    book = ob.get("orderbook_fp", {})
    yes_bids = book.get("yes_dollars", [])
    no_bids  = book.get("no_dollars", [])

    bid = float(yes_bids[0][0]) if yes_bids else None
    ask = (1 - float(no_bids[0][0])) if no_bids else None

    if bid is None or ask is None:
        return None, None

    if bid < MIN_BID:
        print(f"  Skipping: bid {bid:.2f} below minimum {MIN_BID}")
        return None, None

    spread = ask - bid
    if spread > MAX_SPREAD:
        print(f"  Skipping: spread {spread:.2f} exceeds maximum {MAX_SPREAD}")
        return None, None

    return bid, ask
