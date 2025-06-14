import sys, requests

if len(sys.argv) < 2:
    print("No city name has been provideded.")
    sys.exit()

city_name = sys.argv[1]

print(f"Weather forcast for city {city_name}")

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

print(f"Coordinates for {city_name}: {city_coordinates}")

response = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={city_coordinates[0]}&lon={city_coordinates[1]}", headers=headers)

if response.status_code != 200:
    print("Error fetching data from the forecast API. Reason:", response.reason)
    sys.exit()

print(response.json())