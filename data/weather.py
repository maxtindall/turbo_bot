import requests, datetime

def get_weather():
    obs = requests.get("https://api.weather.gov/stations/KPHL/observations/latest").json()
    temp = obs["properties"]["temperature"]["value"] * 9/5 + 32

    meta = requests.get("https://api.weather.gov/points/39.87,-75.24").json()
    forecast = requests.get(meta["properties"]["forecast"]).json()
    high = forecast["properties"]["periods"][0]["temperature"]

    return temp, high, datetime.datetime.now().hour
