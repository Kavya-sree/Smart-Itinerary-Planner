from dotenv import load_dotenv
import os
import googlemaps
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel
import requests
from functools import lru_cache

# Load environment variables
load_dotenv()


SERPER_API_KEY = os.getenv('SERPER_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


if not SERPER_API_KEY or not GOOGLE_MAPS_API_KEY:
    raise ValueError("❌ API keys not found! Please check your .env file.")

# Initialize tools
serper_tool = SerperDevTool()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

@lru_cache(maxsize=100)
def get_lat_lng(address):
    """Fetch latitude and longitude using Google Geocoding API."""
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result and "geometry" in geocode_result[0]:
            location = geocode_result[0]["geometry"]["location"]
            return {"latitude": location["lat"], "longitude": location["lng"]}
    except Exception as e:
        print(f"❌ Geocoding error for '{address}': {e}")
    return None

def get_transportation_details(origin, destination, mode="driving"):
    """Fetch best routes using Google Directions API."""
    origin_coords = get_lat_lng(origin)
    destination_coords = get_lat_lng(destination)

    if not origin_coords or not destination_coords:
        return "❌ Unable to fetch location details."

    url = "https://maps.googleapis.com/maps/api/directions/json"

    payload = {
    "origin": f"{origin_coords['latitude']},{origin_coords['longitude']}",
    "destination": f"{destination_coords['latitude']},{destination_coords['longitude']}",
    "mode": mode.lower(),
    "key": GOOGLE_MAPS_API_KEY
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "routes.legs.distanceMeters,routes.legs.duration"
    }

    try:
        response = requests.get(url, params=payload, headers=headers)
        data = response.json()

        if "routes" in data and data["routes"]:
            route_leg = data["routes"][0]["legs"][0]  # First route's first leg
            distance_km = route_leg.get("distance", {}).get("text", "Unknown")
            duration_str = route_leg.get("duration", {}).get("text", "Unknown")

            return (
                f"🚗 Best route from **{origin}** to **{destination}**:\n"
                f"📏 Distance: {distance_km}\n"
                f"⏳ Duration: {duration_str}"
            )
        return "❌ No route found."

    except requests.RequestException as e:
        return f"⚠️ Network error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# Define input schema
class MapsToolInput(BaseModel):
    origin: str
    destination: str
    mode: str = "driving"

class MapsTool(BaseTool):
    name: str = "Maps Tool"
    description: str = "Provides transportation routes and travel time estimates."
    args_schema = MapsToolInput

    def _run(self, origin: str, destination: str, mode: str = "driving") -> str:
        return get_transportation_details(origin, destination, mode)

# Instantiate the tool
maps_tool = MapsTool()

# Combine all tools
tools = {
    "search": serper_tool,
    "maps": maps_tool
}