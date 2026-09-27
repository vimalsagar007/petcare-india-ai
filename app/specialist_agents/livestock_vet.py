from typing import List, Optional
from app.mcp.tools import mcp_tools
from app.mcp.schemas import ProviderRecord
from app.a2a.messaging import a2a_bus

class LivestockVeterinaryAgent:
    """Agent #5: LivestockVeterinaryAgent - Specializes in Cattle, Buffalo, Goat, Sheep, Horse, & Poultry."""

    async def execute(self, lat: float, lng: float, radius_km: float = 10.0, animal: str = "Cow") -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "LivestockVeterinaryAgent", "REQUEST", {"animal": animal})
        
        raw_providers = await mcp_tools.search_large_animal_vets(lat, lng, radius_km, animal)
        providers = [ProviderRecord(**p) for p in raw_providers]

        a2a_bus.dispatch("LivestockVeterinaryAgent", "CoordinatorAgent", "RESPONSE", {"count": len(providers)})
        return providers

livestock_vet_agent = LivestockVeterinaryAgent()
