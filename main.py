import sys
from rich.console import Console
from rich.table import Table

from weather import process_city_weather

if len(sys.argv) < 2:
    print("No city name has been provideded.")
    sys.exit()

city_names = [sys.argv[1]] if len(sys.argv) == 2 else sys.argv[1:]

rows = []

for city_name in city_names:
    rows.append(process_city_weather(city_name))

table = Table(title=f"Current Weather Information")

columns = ["City name", "Current temperature(Cº/Fº)", "Weather description", "Humidity%", "Wind speed"]

for column in columns:
    table.add_column(column)

for row in rows:
    table.add_row(*row)

console = Console()
console.print(table)