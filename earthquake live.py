import requests

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
data = requests.get(url).json()

for quake in data["features"][:5]:
    place = quake["properties"]["place"]
    mag = quake["properties"]["mag"]
    print(f"🌋 Magnitude {mag} - {place}")