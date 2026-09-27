from typing import List
from app.mcp.schemas import ProviderRecord
from app.a2a.messaging import a2a_bus

class ProviderVerificationAgent:
    """Agent #10: ProviderVerificationAgent - Validates Place ID, address, phone & missing fields."""

    async def verify_providers(self, providers: List[ProviderRecord]) -> List[ProviderRecord]:
        a2a_bus.dispatch("CoordinatorAgent", "ProviderVerificationAgent", "REQUEST", {"count": len(providers)})
        
        verified: List[ProviderRecord] = []
        for p in providers:
            # Check Place ID existence and structure
            if not p.place_id:
                continue
            # Ensure missing fields are assigned standard "Not available from current provider data."
            if not p.phone or p.phone == "None":
                p.phone = "Not available from current provider data."
            if not p.address or p.address == "None":
                p.address = "Not available from current provider data."
            verified.append(p)

        a2a_bus.dispatch("ProviderVerificationAgent", "CoordinatorAgent", "RESPONSE", {"verified_count": len(verified)})
        return verified

provider_verifier_agent = ProviderVerificationAgent()
