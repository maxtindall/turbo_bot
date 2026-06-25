import requests
from config import BASE_URL, KALSHI_API_KEY

headers = {"Authorization": f"Bearer {KALSHI_API_KEY}"}

def get_orderbook(mid):
    return requests.get(f"{BASE_URL}/markets/{mid}/orderbook", headers=headers).json()

def get_bid_ask(ob):
    yes = ob.get("yes", [])
    if not yes:
        return None, None
    best = yes[0]["price"]/100
    return best-0.01, best+0.01
