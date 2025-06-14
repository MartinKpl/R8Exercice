import sys, requests
import time
from rich.console import Console
from rich.table import Table

if len(sys.argv) < 2:
    print("No city name has been provideded.")
    sys.exit()

city_names = [sys.argv[1]] if len(sys.argv) == 2 else sys.argv[1:]

headers = {
    "User-Agent": "PostmanRuntime/7.43.0",
    "Accept": "application/json"
}

rows = []

for city_name in city_names:
    response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json", headers=headers)
    time.sleep(1)  # To avoid hitting the Nominatim API too quickly, they recommend a delay of at least 1 second between requests.

    if response.status_code != 200:
        print("Error fetching data from the GeoCoding API.")
        continue

    data = response.json()

    if len(data) == 0:
        print("No data found for the provided city name.")
        continue

    city_coordinates = data[0].get("lat"), data[0].get("lon")

    if city_coordinates[0] is None or city_coordinates[1] is None:
        print("No coordinates found for the provided city name.")
        continue

    response = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={city_coordinates[0]}&lon={city_coordinates[1]}", headers=headers)

    if response.status_code != 200:
        print("Error fetching data from the forecast API. Reason:", response.reason)
        continue

    timeseries = response.json().get("properties", {}).get("timeseries", [])

    if len(timeseries) == 0:
        print("No weather data found for the provided coordinates.")
        continue

    current_weather_details = timeseries[0].get("data", {}).get("instant", {}).get("details", {})
    weather_description = timeseries[0].get("data", {}).get("next_1_hours", {}).get("summary", {}).get("symbol_code", "N/A")
    
    row = [
        city_name.capitalize(),
        f"{current_weather_details.get('air_temperature', 'N/A')}°C / {current_weather_details.get('air_temperature', 'N/A') * 9/5 + 32:.2f}°F",
        weather_description.replace('_', ' ').capitalize(),
        f"{current_weather_details.get('relative_humidity', 'N/A')}%",
        f"{current_weather_details.get('wind_speed', 'N/A')} m/s"
    ]

    rows.append(row)



table = Table(title=f"Current Weather Information")

columns = ["City name", "Current temperature(Cº/Fº)", "Weather description", "Humidity%", "Wind speed"]

if not current_weather_details:
    print("No current weather details found.")
    sys.exit()

for column in columns:
    table.add_column(column)

for row in rows:
    table.add_row(*row)

console = Console()
console.print(table)