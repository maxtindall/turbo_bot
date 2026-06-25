def estimate(temp, high, threshold, hour):
    """
    Estimate probability that the market resolves YES.

    Args:
        temp:      current temperature (F)
        high:      forecast high for today (F)
        threshold: dict from extract_threshold with keys: type, low, high, mid
        hour:      current hour (0-23)

    Returns:
        float: estimated probability between 0 and 1
    """
    t = threshold["type"]
    mid = threshold["mid"]

    # Use forecast high as best estimate of today's actual high
    # Blend current temp in as the day progresses
    if hour < 10:
        expected = high
    elif hour < 15:
        # Afternoon: blend toward current temp
        weight = (hour - 10) / 5
        expected = high * (1 - weight) + temp * weight
    else:
        # Late day: current temp is close to actual high
        expected = temp

    delta = expected - mid

    if t == "above":
        # YES if high > threshold
        if delta > 4:
            return 0.92
        elif delta > 2:
            return 0.78
        elif delta > 0:
            return 0.60
        elif delta > -2:
            return 0.40
        elif delta > -4:
            return 0.22
        else:
            return 0.08

    elif t == "below":
        # YES if high < threshold (inverse of above)
        if delta < -4:
            return 0.92
        elif delta < -2:
            return 0.78
        elif delta < 0:
            return 0.60
        elif delta < 2:
            return 0.40
        elif delta < 4:
            return 0.22
        else:
            return 0.08

    elif t == "range":
        low = threshold["low"]
        high_bound = threshold["high"]
        # YES if high falls within [low, high_bound]
        if low <= expected <= high_bound:
            return 0.65
        elif abs(expected - mid) <= 2:
            return 0.40
        else:
            return 0.15

    return 0.50
