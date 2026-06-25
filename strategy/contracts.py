import re


def extract_threshold(title):
    """
    Parse a Kalshi Philadelphia temperature market title into a structured dict.

    Handles three formats:
      ">92°"      -> {"type": "above", "low": 92,  "high": None, "mid": 92}
      "<85°"      -> {"type": "below", "low": None, "high": 85,  "mid": 85}
      "85-86°"    -> {"type": "range", "low": 85,  "high": 86,   "mid": 85.5}

    Returns None if no temperature pattern is found.
    """
    # Above threshold: >92°
    m = re.search(r'>(\d+(?:\.\d+)?)[°F]', title)
    if m:
        val = float(m.group(1))
        return {"type": "above", "low": val, "high": None, "mid": val}

    # Below threshold: <85°
    m = re.search(r'<(\d+(?:\.\d+)?)[°F]', title)
    if m:
        val = float(m.group(1))
        return {"type": "below", "low": None, "high": val, "mid": val}

    # Range: 85-86° or 85.5-86.5°
    m = re.search(r'(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)[°F]', title)
    if m:
        low = float(m.group(1))
        high = float(m.group(2))
        return {"type": "range", "low": low, "high": high, "mid": (low + high) / 2}

    return None


def is_philly_weather(title):
    return "Philadelphia" in title and ("Temp" in title or "temp" in title or "°" in title)
