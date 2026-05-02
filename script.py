import requests
from datetime import datetime

LAT = -1.2864
LON = 36.8172

url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"

data = requests.get(url).json()["current_weather"]

temperature = data["temperature"]
windspeed = data["windspeed"]
weathercode = data["weathercode"]

mapping = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast"
}

condition = mapping.get(weathercode, "Unknown")

today = datetime.now().strftime("%Y-%m-%d")

report = f"""
Weather Dashboard - Nairobi

Date: {today}

Temperature: {temperature}°C
Wind Speed: {windspeed} km/h
Condition: {condition}
"""

with open("dashboard.md", "w") as f:
    f.write(report)