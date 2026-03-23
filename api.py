import requests
from urllib.parse import quote

API_KEY = "fc52bf9fcfc628b0ecaa42719bd20945eafd68bc1q5mlw63yd2u2cn0hs6jnzf2gljhr486u3dkgm2y"

def get_bbox(city):
    url = f"https://nominatim.openstreetmap.org/search?q={quote(city)}&format=json"
    headers = {"User-Agent": "OpenAQ"}

    response = requests.get(url).json()

    bbox = response[0]["boundingbox"]
    min_lat, max_lat, min_lon, max_lon = bbox

    return f"{min_lon},{min_lat},{max_lon},{max_lat}"


def get_locations(bbox):
    url = f"https://api.openaq.org/v3/locations?bbox={bbox}"
    headers = {"X-API-Key": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()["results"]

    return []