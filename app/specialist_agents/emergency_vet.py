from typing import List, Dict, Any, Optional
from app.mcp.tools import mcp_tools
from app.mcp.schemas import ProviderRecord
from app.safety.guardrails import safety_guardrails
from app.a2a.messaging import a2a_bus

class EmergencyVeterinaryAgent:
    """Agent #6: EmergencyVeterinaryAgent - Prioritizes 24/7 emergency facilities and warnings."""

    async def execute(self, query: str, lat: float, lng: float, radius_km: float = 10.0, animal: Optional[str] = None) -> Dict[str, Any]:
        a2a_bus.dispatch("CoordinatorAgent", "EmergencyVeterinaryAgent", "REQUEST", {"query": query, "animal": animal})

        is_emergency, warning = safety_guardrails.check_emergency(query)
        
        # Search emergency facilities
        raw_providers = await mcp_tools.search_emergency_veterinarians(lat, lng, radius_km, animal)
        providers = [ProviderRecord(**p) for p in raw_providers]

        # Ensure open facilities are sorted first
        providers.sort(key=lambda p: (not p.open_now, p.distance_km))

        response = {
            "is_emergency": True,
            "warning": warning or "EMERGENCY: Please seek immediate evaluation at a 24/7 veterinary facility.",
            "providers": providers
        }
        a2a_bus.dispatch("EmergencyVeterinaryAgent", "CoordinatorAgent", "RESPONSE", {"provider_count": len(providers)})
        return response

emergency_vet_agent = EmergencyVeterinaryAgent()
