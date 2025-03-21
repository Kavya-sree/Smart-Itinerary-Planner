from dotenv import load_dotenv
load_dotenv()
import os
import googlemaps
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from pydantic import BaseModel



os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')



# Initialize the Internet search tool
serper_tool = SerperDevTool()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))


import requests
import os

def get_transportation_details(origin, destination, mode="DRIVE"):
    """Fetch best routes using Google Routes API."""
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": mode.upper()
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.legs.distanceMeters,routes.legs.duration"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if "routes" in data and data["routes"]:
            route = data["routes"][0]["legs"][0]
            distance_km = route["distanceMeters"] / 1000
            duration_sec = int(route["duration"].replace('s', ''))  # Convert "147378s" to int
            
            hours, remainder = divmod(duration_sec, 3600)
            minutes, _ = divmod(remainder, 60)
            duration_str = f"{hours}h {minutes}m"

            return f"🚗 Best route from {origin} to {destination}: {distance_km} km, estimated time: {duration_str}."
        
        return "No route found."
    
    except Exception as e:
        return f"Error fetching route: {e}"
    
# Define input schema
class MapsToolInput(BaseModel):
    origin: str
    destination: str
    mode: str = "DRIVE"

class MapsTool(BaseTool):
    name: str = "Maps Tool"
    description: str = "Provides transportation routes and travel time estimates."
    args_schema = MapsToolInput  # Define the expected parameters

    def _run(self, origin: str, destination: str, mode: str = "DRIVE") -> str:
        """Implements the abstract _run method."""
        return get_transportation_details(origin, destination, mode)

# Instantiate the tool
maps_tool = MapsTool()

# Combine all tools
tools = {
    "search": serper_tool,
    "maps": maps_tool
}
