import requests
import time

headers = {
    "User-Agent": "PostmanRuntime/7.43.0",
    "Accept": "application/json"
}

city_coordinates_cache = {}
weather_data_cache = {}

def get_city_coordinates(city_name: str):
    if city_name.lower() in city_coordinates_cache:
        return city_coordinates_cache[city_name.lower()]

    response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json", headers=headers)
    time.sleep(1)  # To avoid hitting the Nominatim API too quickly, they recommend a delay of at least 1 second between requests.

    if response.status_code != 200:
        print("Error fetching data from the GeoCoding API.")
        return None
    data = response.json()

    if len(data) == 0:
        print(f"No data found for {city_name}.")
        return None
    
    city_coordinates_cache[city_name.lower()] = data[0].get("lat"), data[0].get("lon")
    return data[0].get("lat"), data[0].get("lon")

def get_weather_data(city_coordinates):
    if city_coordinates[0] is None or city_coordinates[1] is None:
        return None
    
    coord_key = f"{city_coordinates[0]},{city_coordinates[1]}"
    if coord_key in weather_data_cache:
        return weather_data_cache[coord_key]


    response = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={city_coordinates[0]}&lon={city_coordinates[1]}", headers=headers)

    if response.status_code != 200:
        print("Error fetching data from the forecast API. Reason:", response.reason)
        return None

    weather_data_cache[coord_key] = response.json()
    return response.json()

def parse_weather_data(city_name, current_weather_details, weather_description):
    return [
        city_name.capitalize(),
        f"{current_weather_details.get('air_temperature', 'N/A')}°C / {current_weather_details.get('air_temperature', 'N/A') * 9/5 + 32:.2f}°F",
        weather_description.replace('_', ' ').capitalize(),
        f"{current_weather_details.get('relative_humidity', 'N/A')}%",
        f"{current_weather_details.get('wind_speed', 'N/A')} m/s"
    ]

def process_city_weather(city_name):
    city_coordinates = get_city_coordinates(city_name)

    if not city_coordinates:
        print(f"No coordinates found for the provided city name: {city_name}")
        return None

    weather_data = get_weather_data(city_coordinates)

    if not weather_data:
        print(f"No weather data found for {city_name}.")
        return None

    timeseries = weather_data.get("properties", {}).get("timeseries", [])
    if not timeseries or len(timeseries) == 0:
        print(f"No weather data found for the provided coordinates of {city_name}.")
        return None
    
    current_weather_details = timeseries[0].get("data", {}).get("instant", {}).get("details", {})
    weather_description = timeseries[0].get("data", {}).get("next_1_hours", {}).get("summary", {}).get("symbol_code", "N/A")

    return parse_weather_data(city_name, current_weather_details, weather_description)