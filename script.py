import requests
import json
import os
from datetime import datetime

# --- Load config ---
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    # Fallback defaults
    return {
        "city": "Nairobi",
        "latitude": -1.2864,
        "longitude": 36.8172,
        "dashboard_file": "dashboard.md",
        "history_dir": "history"
    }

# --- Weather code mapping (full WMO codes) ---
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def fetch_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=relativehumidity_2m,precipitation_probability,uv_index"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def parse_weather(data):
    current = data["current_weather"]
    hourly = data.get("hourly", {})

    # Pull the first hourly values as a proxy for current conditions
    humidity = hourly.get("relativehumidity_2m", [None])[0]
    precip_prob = hourly.get("precipitation_probability", [None])[0]
    uv_index = hourly.get("uv_index", [None])[0]

    return {
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "weathercode": current["weathercode"],
        "condition": WEATHER_CODES.get(current["weathercode"], f"Code {current['weathercode']}"),
        "humidity": humidity,
        "precip_probability": precip_prob,
        "uv_index": uv_index,
    }

def build_report(city, weather, date_str):
    humidity_line = f"Humidity:              {weather['humidity']}%" if weather['humidity'] is not None else ""
    precip_line   = f"Precipitation Chance:  {weather['precip_probability']}%" if weather['precip_probability'] is not None else ""
    uv_line       = f"UV Index:              {weather['uv_index']}" if weather['uv_index'] is not None else ""

    extras = "\n".join(line for line in [humidity_line, precip_line, uv_line] if line)

    return f"""## Weather Dashboard — {city}

**Date:** {date_str}

| Metric | Value |
|---|---|
| Temperature | {weather['temperature']}°C |
| Wind Speed | {weather['windspeed']} km/h |
| Condition | {weather['condition']} |
| Humidity | {weather['humidity']}% |
| Precipitation Chance | {weather['precip_probability']}% |
| UV Index | {weather['uv_index']} |

---
"""

def write_dashboard(report, filepath):
    with open(filepath, "w") as f:
        f.write(report)

def append_to_history(report, history_dir, date_str):
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, f"{date_str}.md")
    with open(history_file, "w") as f:
        f.write(report)

    # Also append a one-line summary to the history log
    log_file = os.path.join(history_dir, "log.md")
    with open(log_file, "a") as f:
        f.write(f"| {date_str} | {report.split('Temperature')[0]} |\n")  # placeholder

def append_summary_to_log(weather, city, date_str, history_dir):
    os.makedirs(history_dir, exist_ok=True)
    log_file = os.path.join(history_dir, "log.md")
    # Write header if file is new
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        with open(log_file, "w") as f:
            f.write("# Weather History Log\n\n")
            f.write("| Date | Temp (°C) | Wind (km/h) | Condition | Humidity | Precip % | UV |\n")
            f.write("|---|---|---|---|---|---|---|\n")
    with open(log_file, "a") as f:
        f.write(
            f"| {date_str} | {weather['temperature']} | {weather['windspeed']} "
            f"| {weather['condition']} | {weather['humidity']}% "
            f"| {weather['precip_probability']}% | {weather['uv_index']} |\n"
        )

def main():
    config = load_config()
    city        = config["city"]
    lat         = config["latitude"]
    lon         = config["longitude"]
    dashboard   = config["dashboard_file"]
    history_dir = config["history_dir"]

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        raw_data = fetch_weather(lat, lon)
        weather  = parse_weather(raw_data)
        report   = build_report(city, weather, today)

        # 1. Overwrite dashboard.md with latest
        write_dashboard(report, dashboard)

        # 2. Save daily file to history/YYYY-MM-DD.md
        daily_path = os.path.join(history_dir, f"{today}.md")
        os.makedirs(history_dir, exist_ok=True)
        write_dashboard(report, daily_path)

        # 3. Append one-line summary to history/log.md
        append_summary_to_log(weather, city, today, history_dir)

        print(f"Weather report written for {city} on {today}")

    except requests.exceptions.Timeout:
        error_msg = f"Weather fetch failed on {today}: Request timed out.\n"
        with open(dashboard, "w") as f:
            f.write(error_msg)
        print(error_msg)
        raise

    except requests.exceptions.HTTPError as e:
        error_msg = f" Weather fetch failed on {today}: HTTP error — {e}\n"
        with open(dashboard, "w") as f:
            f.write(error_msg)
        print(error_msg)
        raise

    except Exception as e:
        error_msg = f" Weather fetch failed on {today}: {e}\n"
        with open(dashboard, "w") as f:
            f.write(error_msg)
        print(error_msg)
        raise

if __name__ == "__main__":
    main()