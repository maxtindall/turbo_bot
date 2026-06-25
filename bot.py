from kalshi.discovery import get_phl_markets
from kalshi.market import get_orderbook, get_bid_ask
from data.weather import get_weather
from strategy.model import estimate
from strategy.contracts import extract_threshold
from execution.engine import place
from execution.positions import get_position, update


def run():
    print("BOT START")
    print("Fetching markets...")

    markets = get_phl_markets()

    print("Returned from market fetch")

    if not markets:
        print("No markets found -- exiting")
        print("BOT END")
        return

    print(f"\nUSING {len(markets)} MARKETS")

    try:
        temp, high, hour = get_weather()
        print("Weather:", temp, high, hour)
    except Exception as e:
        print("WEATHER FETCH FAILED:", e)
        print("BOT END")
        return

    for m in markets:
        print("\n======================")
        print("Processing:", m["title"])

        mid = m["ticker"]
        threshold = extract_threshold(m["title"])
        print("Threshold:", threshold)

        if not threshold:
            print("No threshold found, skipping")
            continue

        try:
            ob = get_orderbook(mid)
            print("Orderbook:", ob)

            bid, ask = get_bid_ask(ob)
            print("Bid/Ask:", bid, ask)

        except Exception as e:
            print("ORDERBOOK ERROR:", e)
            continue

        if bid is None:
            print("  No tradeable market, skipping")
            continue

        try:
            model_p = estimate(temp, high, threshold, hour)
            edge = model_p - bid

            print(
                "Model:", round(model_p, 3),
                "| Market:", round(bid, 3),
                "| Edge:", round(edge, 3)
            )
        except Exception as e:
            print("MODEL ERROR:", e)
            continue

        try:
            pos = get_position(mid)
            print("Position:", pos)
        except Exception as e:
            print("POSITION ERROR:", e)
            pos = None

        if edge > 0.05 and pos != "YES":
            print("TRADE YES")
            place(mid, "YES", bid)
            update(mid, "YES")

        elif edge < -0.05 and pos != "NO":
            print("TRADE NO")
            place(mid, "NO", ask if ask else (1 - bid))
            update(mid, "NO")

        else:
            print("No trade")

    print("\nBOT END")


if __name__ == "__main__":
    run()
