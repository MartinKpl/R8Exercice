import sys, requests
from rich.console import Console
from rich.table import Table

if len(sys.argv) < 2:
    print("No city name has been provideded.")
    sys.exit()

city_name = sys.argv[1]

headers = {
    "User-Agent": "PostmanRuntime/7.43.0",
    "Accept": "application/json"
}

response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json", headers=headers)

if response.status_code != 200:
    print("Error fetching data from the GeoCoding API.")
    sys.exit()

data = response.json()

if len(data) == 0:
    print("No data found for the provided city name.")
    sys.exit()

city_coordinates = data[0].get("lat"), data[0].get("lon")

if city_coordinates[0] is None or city_coordinates[1] is None:
    print("No coordinates found for the provided city name.")
    sys.exit()

response = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={city_coordinates[0]}&lon={city_coordinates[1]}", headers=headers)

if response.status_code != 200:
    print("Error fetching data from the forecast API. Reason:", response.reason)
    sys.exit()

timeseries = response.json().get("properties", {}).get("timeseries", [])

if len(timeseries) == 0:
    print("No weather data found for the provided coordinates.")
    sys.exit()



table = Table(title=f"Weather Forecast for {city_name.capitalize()}")

columns = ["City name", "Current temperature(Cº/Fº)", "Weather description", "Humidity%", "Wind speed"]

current_weather_details = timeseries[0].get("data", {}).get("instant", {}).get("details", {})
weather_description = timeseries[0].get("data", {}).get("next_1_hours", {}).get("summary", {}).get("symbol_code", "N/A")

if not current_weather_details:
    print("No current weather details found.")
    sys.exit()

row = [
    city_name.capitalize(),
    f"{current_weather_details.get('air_temperature', 'N/A')}°C / {current_weather_details.get('air_temperature', 'N/A') * 9/5 + 32:.2f}°F",
    weather_description.replace('_', ' ').capitalize(),
    f"{current_weather_details.get('relative_humidity', 'N/A')}%",
    f"{current_weather_details.get('wind_speed', 'N/A')} m/s"
]

for column in columns:
    table.add_column(column)

table.add_row(*row, style='bright_green')

console = Console()
console.print(table)