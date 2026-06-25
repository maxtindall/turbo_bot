def estimate(temp, high, threshold, hour):
    if hour < 12:
        return 0.55 if high >= threshold else 0.45
    elif hour < 16:
        return 0.7 if temp > threshold-2 else 0.3
    else:
        return 0.95 if temp >= threshold else 0.05
