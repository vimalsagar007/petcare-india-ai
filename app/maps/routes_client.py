import httpx
import math
from typing import Dict, Tuple, Optional, Any

# Indian City Geocoding Coordinate Database for real-time fallback resolution
INDIAN_CITIES_GEOCODE: Dict[str, Tuple[float, float]] = {
    "hyderabad": (17.3850, 78.4867),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "guntur": (16.3067, 80.4365),
    "vijayawada": (16.5062, 80.6480),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "chandigarh": (30.7333, 76.7794),
    "coimbatore": (11.0168, 76.9558),
    "kochi": (9.9312, 76.2673),
    "bhopal": (23.2599, 77.4126),
    "patna": (25.5941, 85.1376),
    "surat": (21.1702, 72.8311)
}

class RoutesClient:
    """Client for Geocoding and Google Maps Directions links."""

    @staticmethod
    def geocode_location(location_name: str) -> Tuple[float, float]:
        clean_loc = location_name.lower().strip()
        
        # Check coordinate format (lat, lng)
        if "," in clean_loc:
            parts = clean_loc.split(",")
            try:
                return float(parts[0].strip()), float(parts[1].strip())
            except ValueError:
                pass

        # Match known Indian cities
        for city_key, coords in INDIAN_CITIES_GEOCODE.items():
            if city_key in clean_loc or clean_loc in city_key:
                return coords

        # Dynamic fallback centered on India (Hyderabad center)
        return 17.3850, 78.4867

    @staticmethod
    def generate_google_maps_directions_url(
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        destination_name: str = ""
    ) -> str:
        base_url = "https://www.google.com/maps/dir/?api=1"
        origin = f"{origin_lat},{origin_lng}"
        destination = f"{dest_lat},{dest_lng}"
        return f"{base_url}&origin={origin}&destination={destination}&travelmode=driving"

    def calculate_travel_info(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float
    ) -> Dict[str, Any]:
        R = 6371.0
        dlat = math.radians(dest_lat - origin_lat)
        dlon = math.radians(dest_lng - origin_lng)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(origin_lat)) * math.cos(math.radians(dest_lat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = round(R * c, 2)
        est_minutes = int(dist_km * 2.5) + 3

        return {
            "distance_km": dist_km,
            "estimated_driving_time_minutes": est_minutes,
            "google_maps_directions_url": self.generate_google_maps_directions_url(origin_lat, origin_lng, dest_lat, dest_lng)
        }

routes_client = RoutesClient()
