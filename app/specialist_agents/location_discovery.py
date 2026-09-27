from typing import Dict, Any, List, Optional
from app.mcp.tools import mcp_tools
from app.mcp.schemas import ProviderRecord
from app.a2a.messaging import a2a_bus

class LocationDiscoveryAgent:
    """Agent #1: LocationDiscoveryAgent - Finds nearby veterinary providers by radius & species."""

    async def execute(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        category: str = "all",
        animal: Optional[str] = None
    ) -> List[ProviderRecord]:
        
        a2a_bus.dispatch("CoordinatorAgent", "LocationDiscoveryAgent", "REQUEST", {
            "lat": lat, "lng": lng, "radius_km": radius_km, "category": category, "animal": animal
        })

        providers_raw: List[Dict[str, Any]] = []

        if category == "emergency":
            providers_raw = await mcp_tools.search_emergency_veterinarians(lat, lng, radius_km, animal)
        elif category == "government":
            providers_raw = await mcp_tools.search_government_veterinary_hospitals(lat, lng, radius_km, animal)
        elif category == "large_animal":
            providers_raw = await mcp_tools.search_large_animal_vets(lat, lng, radius_km, animal)
        elif category == "avian":
            providers_raw = await mcp_tools.search_avian_vets(lat, lng, radius_km)
        elif category == "diagnostics":
            providers_raw = await mcp_tools.search_animal_diagnostics(lat, lng, radius_km)
        elif category == "pharmacy":
            providers_raw = await mcp_tools.search_pet_pharmacies(lat, lng, radius_km)
        elif category == "ambulance":
            providers_raw = await mcp_tools.search_animal_ambulances(lat, lng, radius_km)
        else:
            providers_raw = await mcp_tools.search_nearby_veterinary_hospitals(lat, lng, radius_km, animal)

        records = [ProviderRecord(**p) for p in providers_raw]
        a2a_bus.dispatch("LocationDiscoveryAgent", "CoordinatorAgent", "RESPONSE", {"count": len(records)})
        return records

location_discovery_agent = LocationDiscoveryAgent()
