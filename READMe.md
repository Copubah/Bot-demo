# Bot-demo Daily Weather Bot

A lightweight Python bot that fetches real-time weather data for Nairobi, Kenya and writes a formatted daily report to `dashboard.md`. Runs automatically on a schedule via GitHub Actions no manual intervention needed.

---

## How It Works

1. `script.py` calls the [Open-Meteo API](https://open-meteo.com/) (free, no API key required) using Nairobi's coordinates.
2. It extracts temperature,wind speed, and a weather condition mapped from the WMO weather code.
3. The report is written to `dashboard.md` with the current date, overwriting the previous day's entry.
4. A GitHub Actions workflow triggers the script on a defined schedule (e.g., daily at 06:00 UTC).

---

## Sample Output (`dashboard.md`)

```
Weather Dashboard - Nairobi
Date: 2026-06-28
Temperature: 19.2°C
Wind Speed: 14.5 km/h
Condition: Partly cloudy
```

---

## Project Structure

```
Bot-demo/
├── .github/
│   └── workflows/
│       └── weather.yml      # GitHub Actions workflow (scheduled trigger)
├── script.py                # Main bot script
├── dashboard.md             # Auto-generated weather report (updated daily)
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- `requests` library

### Run Locally

```bash
# Clone the repo
git clone https://github.com/Copubah/Bot-demo.git
cd Bot-demo

# Install dependency
pip install requests

# Run the bot
python script.py

# Check the output
cat dashboard.md
```

---

## GitHub Actions (Automated Scheduling)

The workflow in `.github/workflows/weather.yml` runs the script on a cron schedule. No secrets or API keys are required since Open-Meteo is a public, free API.

To change the location, update the coordinates in `script.py`:

```python
LAT = -1.2864   # Latitude
LON = 36.8172   # Longitude (currently set to Nairobi, Kenya)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Bot logic |
| [Open-Meteo API](https://open-meteo.com/) | Free weather data (no key needed) |
| GitHub Actions | Scheduled automation (CI/CD) |
| Markdown | Output report format |

---



## License

This project is open source and available under the [MIT License](LICENSE).