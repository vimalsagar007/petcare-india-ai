from typing import Dict, Any
from app.maps.routes_client import routes_client
from app.a2a.messaging import a2a_bus

class NavigationAgent:
    """Agent #9: NavigationAgent - Routes calculation & Google Maps navigation links."""

    async def execute(self, origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> Dict[str, Any]:
        a2a_bus.dispatch("CoordinatorAgent", "NavigationAgent", "REQUEST", {"origin": (origin_lat, origin_lng), "dest": (dest_lat, dest_lng)})
        
        info = routes_client.calculate_travel_info(origin_lat, origin_lng, dest_lat, dest_lng)
        
        a2a_bus.dispatch("NavigationAgent", "CoordinatorAgent", "RESPONSE", info)
        return info

navigation_agent = NavigationAgent()
