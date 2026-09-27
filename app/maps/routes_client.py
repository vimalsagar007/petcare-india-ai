import math
from typing import Dict, Any, Tuple
from app.mcp.schemas import LocationCoordinates

CITY_COORDINATES: Dict[str, Tuple[float, float]] = {
    "hyderabad": (17.3850, 78.4867),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "delhi ncr": (28.6139, 77.2090),
    "pune": (18.5204, 73.8567),
    "kolkata": (22.5726, 88.3639),
    "ahmedabad": (23.0225, 72.5714),
    "guntur": (16.3067, 80.4365),
    "vijayawada": (16.5062, 80.6480),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "warangal": (17.9689, 79.5941),
    "tirupati": (13.6288, 79.4192),
    "nellore": (14.4426, 79.9865)
}

class RoutesClient:
    """Routes and navigation client generating Google Maps links and estimated driving time."""

    def geocode_location(self, location_text: str) -> LocationCoordinates:
        loc_clean = location_text.strip().lower()
        for city, coords in CITY_COORDINATES.items():
            if city in loc_clean:
                return LocationCoordinates(latitude=coords[0], longitude=coords[1])
        # Default to Hyderabad central if unknown
        return LocationCoordinates(latitude=17.3850, longitude=78.4867)

    def calculate_travel_info(self, origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> Dict[str, Any]:
        dlat = math.radians(dest_lat - origin_lat)
        dlon = math.radians(dest_lng - origin_lng)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(origin_lat)) * math.cos(math.radians(dest_lat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = round(6371.0 * c, 2)
        
        # Estimate travel time based on typical Indian urban driving speed (25 km/h)
        est_minutes = max(2, int((dist_km / 25.0) * 60))
        
        maps_link = f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&travelmode=driving"
        
        return {
            "distance_km": dist_km,
            "estimated_minutes": est_minutes,
            "travel_mode": "driving",
            "google_maps_directions_url": maps_link
        }

routes_client = RoutesClient()
