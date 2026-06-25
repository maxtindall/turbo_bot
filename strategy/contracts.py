import re

def extract_threshold(title):
    match = re.search(r'(\d{2,3})F', title)
    if match:
        return int(match.group(1))
    return None

def is_philly_weather(title):
    return "Philadelphia" in title and "Temp" in title
