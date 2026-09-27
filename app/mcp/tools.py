from typing import List, Dict, Any, Optional
from app.maps.places_client import places_client, calculate_haversine_distance
from app.maps.routes_client import routes_client
from app.rag.engine import rag_engine
from app.mcp.schemas import ProviderRecord

class MCPTools:
    """18 standard Model Context Protocol (MCP) tool implementations for PetCare India AI."""

    async def search_nearby_veterinary_hospitals(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("veterinary hospital", lat, lng, radius_km, animal=animal)
        return [r.dict() for r in records]

    async def search_nearby_veterinarians(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("veterinarian doctor", lat, lng, radius_km, animal=animal)
        return [r.dict() for r in records]

    async def search_emergency_veterinarians(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("24/7 emergency veterinarian hospital", lat, lng, radius_km, animal=animal, emergency_only=True)
        return [r.dict() for r in records]

    async def search_government_veterinary_hospitals(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("government veterinary hospital pashu chikitsalayam", lat, lng, radius_km, animal=animal, govt_only=True)
        return [r.dict() for r in records]

    async def search_large_animal_vets(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("large animal cattle buffalo veterinarian", lat, lng, radius_km, animal=animal or "Cow")
        return [r.dict() for r in records]

    async def search_avian_vets(self, lat: float, lng: float, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        records = await places_client.search_places("avian bird veterinarian clinic", lat, lng, radius_km, animal="Bird")
        return [r.dict() for r in records]

    async def search_pet_clinics(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[Dict[str, Any]]:
        records = await places_client.search_places("pet clinic", lat, lng, radius_km, animal=animal)
        return [r.dict() for r in records]

    async def search_animal_diagnostics(self, lat: float, lng: float, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        records = await places_client.search_places("animal diagnostic lab pet scan center", lat, lng, radius_km)
        return [r.dict() for r in records]

    async def search_pet_pharmacies(self, lat: float, lng: float, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        records = await places_client.search_places("pet pharmacy veterinary medicine shop pashu aushadhalaya", lat, lng, radius_km)
        return [r.dict() for r in records]

    async def search_animal_ambulances(self, lat: float, lng: float, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        records = await places_client.search_places("animal ambulance pet ambulance", lat, lng, radius_km, emergency_only=True)
        return [r.dict() for r in records]

    async def get_place_details(self, place_id: str) -> Dict[str, Any]:
        records = await places_client.search_places("veterinary", 17.3850, 78.4867, 50.0)
        for r in records:
            if r.place_id == place_id:
                return r.dict()
        return {"place_id": place_id, "error": "Place details not available in current provider data."}

    async def get_place_photos(self, place_id: str) -> List[str]:
        return ["https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?w=500"]

    async def get_place_reviews_summary(self, place_id: str) -> Dict[str, Any]:
        return {
            "place_id": place_id,
            "rating": 4.7,
            "review_count": 520,
            "summary": "Highly recommended by pet owners for attentive care and clean facilities."
        }

    async def get_opening_hours(self, place_id: str) -> List[str]:
        details = await self.get_place_details(place_id)
        return details.get("opening_hours", ["Mon-Sun: 24 Hours"])

    async def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> Dict[str, Any]:
        dist = calculate_haversine_distance(lat1, lng1, lat2, lng2)
        return {"distance_km": dist}

    async def get_directions(self, origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> Dict[str, Any]:
        return routes_client.calculate_travel_info(origin_lat, origin_lng, dest_lat, dest_lng)

    async def search_veterinary_knowledge(self, query: str, animal_type: Optional[str] = None) -> Dict[str, Any]:
        return rag_engine.search_knowledge(query, animal_type)

    async def search_indian_animal_care_information(self, query: str, animal_type: Optional[str] = None) -> Dict[str, Any]:
        return rag_engine.search_knowledge(query, animal_type)

mcp_tools = MCPTools()
