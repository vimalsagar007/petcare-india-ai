from typing import List, Optional
from app.mcp.tools import mcp_tools
from app.mcp.schemas import ProviderRecord
from app.a2a.messaging import a2a_bus

class GovernmentVeterinaryAgent:
    """Agent #7: GovernmentVeterinaryAgent - Searches Govt Veterinary Hospitals, Dispensaries & Animal Husbandry."""

    async def execute(self, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "GovernmentVeterinaryAgent", "REQUEST", {"lat": lat, "lng": lng, "animal": animal})
        
        raw_govt = await mcp_tools.search_government_veterinary_hospitals(lat, lng, radius_km, animal)
        providers = [ProviderRecord(**p) for p in raw_govt]

        a2a_bus.dispatch("GovernmentVeterinaryAgent", "CoordinatorAgent", "RESPONSE", {"count": len(providers)})
        return providers

govt_vet_agent = GovernmentVeterinaryAgent()
