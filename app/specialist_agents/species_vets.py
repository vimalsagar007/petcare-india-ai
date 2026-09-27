from typing import List, Optional
from app.mcp.tools import mcp_tools
from app.mcp.schemas import ProviderRecord
from app.a2a.messaging import a2a_bus

class DogVeterinaryAgent:
    """Agent #2: DogVeterinaryAgent - Specializes in Canine care & clinics."""
    async def execute(self, lat: float, lng: float, radius_km: float = 10.0) -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "DogVeterinaryAgent", "REQUEST", {"animal": "Dog"})
        raw = await mcp_tools.search_nearby_veterinarians(lat, lng, radius_km, animal="Dog")
        return [ProviderRecord(**p) for p in raw]

class CatVeterinaryAgent:
    """Agent #3: CatVeterinaryAgent - Specializes in Feline care & clinics."""
    async def execute(self, lat: float, lng: float, radius_km: float = 10.0) -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "CatVeterinaryAgent", "REQUEST", {"animal": "Cat"})
        raw = await mcp_tools.search_nearby_veterinarians(lat, lng, radius_km, animal="Cat")
        return [ProviderRecord(**p) for p in raw]

class AvianVeterinaryAgent:
    """Agent #4: AvianVeterinaryAgent - Specializes in Bird & Exotic animal care."""
    async def execute(self, lat: float, lng: float, radius_km: float = 10.0) -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "AvianVeterinaryAgent", "REQUEST", {"animal": "Bird"})
        raw = await mcp_tools.search_avian_vets(lat, lng, radius_km)
        return [ProviderRecord(**p) for p in raw]

dog_vet_agent = DogVeterinaryAgent()
cat_vet_agent = CatVeterinaryAgent()
avian_vet_agent = AvianVeterinaryAgent()
