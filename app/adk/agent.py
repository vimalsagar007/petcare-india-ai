import time
import uuid
from typing import Dict, Any, List, Optional
from app.config import settings
from app.mcp.schemas import AgentResponse, ProviderRecord, RAGSourceCitation
from app.adk.router import router_logic
from app.adk.observability import LatencyTracker
from app.specialist_agents.location_discovery import location_discovery_agent
from app.specialist_agents.emergency_vet import emergency_vet_agent
from app.specialist_agents.govt_vet import govt_vet_agent
from app.specialist_agents.livestock_vet import livestock_vet_agent
from app.specialist_agents.species_vets import dog_vet_agent, cat_vet_agent, avian_vet_agent
from app.specialist_agents.rag_vet import rag_vet_agent
from app.specialist_agents.provider_verifier import provider_verifier_agent
from app.specialist_agents.navigation import navigation_agent

class PetCareCoordinatorAgent:
    """Root Google ADK Coordinator Agent for PetCare India AI."""

    async def process_user_request(
        self,
        query: str,
        animal: Optional[str] = None,
        location_text: Optional[str] = None,
        radius_km: float = 10.0,
        urgency: Optional[str] = None,
        language: Optional[str] = None,
        session_id: str = "default_session"
    ) -> AgentResponse:
        
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        tracker = LatencyTracker(request_id, session_id)
        tracker.record_agent("PetCareCoordinatorAgent")

        # Step 1: Parse intent and routing parameters
        t0 = time.time()
        parsed = router_logic.parse_query(query, animal, location_text)
        tracker.record_gemini((time.time() - t0) * 1000.0)

        effective_animal = animal or parsed["animal"]
        effective_lang = language or parsed["language"]
        effective_urgency = urgency or parsed["urgency"]
        is_emergency = parsed["is_emergency"] or effective_urgency == "Emergency"

        providers: List[ProviderRecord] = []
        rag_answer: Optional[str] = None
        citations: List[RAGSourceCitation] = []
        emergency_warning: Optional[str] = None

        # Step 2: Emergency Workflow
        if is_emergency:
            tracker.record_agent("EmergencyVeterinaryAgent")
            t_em = time.time()
            em_res = await emergency_vet_agent.execute(query, parsed["latitude"], parsed["longitude"], radius_km, effective_animal)
            tracker.record_tool("search_emergency_veterinarians", (time.time() - t_em) * 1000.0)
            
            emergency_warning = em_res.get("warning")
            providers = em_res.get("providers", [])

        # Step 3: Service & Provider Discovery Workflow
        if not providers and parsed["needs_maps"]:
            category = parsed["category"]
            t_loc = time.time()

            if category == "government":
                tracker.record_agent("GovernmentVeterinaryAgent")
                providers = await govt_vet_agent.execute(parsed["latitude"], parsed["longitude"], radius_km, effective_animal)
            elif category == "large_animal" or effective_animal in ["Cow", "Buffalo", "Goat", "Sheep", "Horse", "Poultry"]:
                tracker.record_agent("LivestockVeterinaryAgent")
                providers = await livestock_vet_agent.execute(parsed["latitude"], parsed["longitude"], radius_km, effective_animal)
            elif category == "avian" or effective_animal == "Bird":
                tracker.record_agent("AvianVeterinaryAgent")
                providers = await avian_vet_agent.execute(parsed["latitude"], parsed["longitude"], radius_km)
            elif effective_animal == "Dog":
                tracker.record_agent("DogVeterinaryAgent")
                providers = await dog_vet_agent.execute(parsed["latitude"], parsed["longitude"], radius_km)
            elif effective_animal == "Cat":
                tracker.record_agent("CatVeterinaryAgent")
                providers = await cat_vet_agent.execute(parsed["latitude"], parsed["longitude"], radius_km)
            else:
                tracker.record_agent("LocationDiscoveryAgent")
                providers = await location_discovery_agent.execute(parsed["latitude"], parsed["longitude"], radius_km, category, effective_animal)

            tracker.record_tool("search_places", (time.time() - t_loc) * 1000.0)

            # Step 4: Radius Expansion Fallback Strategy
            if not providers and radius_km < 25.0:
                expanded_radius = 25.0
                tracker.record_fallback(f"No provider found within {radius_km} km. Expanding radius to {expanded_radius} km.")
                providers = await location_discovery_agent.execute(parsed["latitude"], parsed["longitude"], expanded_radius, category, effective_animal)

        # Step 5: Provider Verification Agent
        if providers:
            tracker.record_agent("ProviderVerificationAgent")
            providers = await provider_verifier_agent.verify_providers(providers)

            # Generate driving directions via NavigationAgent for top provider
            if len(providers) > 0:
                tracker.record_agent("NavigationAgent")
                t_nav = time.time()
                top_p = providers[0]
                nav_info = await navigation_agent.execute(parsed["latitude"], parsed["longitude"], top_p.location.latitude, top_p.location.longitude)
                top_p.maps_url = nav_info.get("google_maps_directions_url")
                tracker.record_tool("get_directions", (time.time() - t_nav) * 1000.0)

        # Step 6: Veterinary RAG Agent Workflow
        if parsed["needs_rag"] or not providers:
            tracker.record_agent("VeterinaryRAGAgent")
            t_rag = time.time()
            rag_res = await rag_vet_agent.execute(query, effective_animal)
            tracker.record_rag((time.time() - t_rag) * 1000.0)
            
            rag_answer = rag_res.get("answer")
            citations = [RAGSourceCitation(**c) for c in rag_res.get("citations", [])]

        # Step 7: Construct Grounded Final Response
        return AgentResponse(
            request_id=request_id,
            session_id=session_id,
            user_query=query,
            language=effective_lang,
            animal_detected=effective_animal,
            urgency_level=effective_urgency,
            agent_chain=tracker.agent_selected,
            is_emergency=is_emergency,
            emergency_warning=emergency_warning,
            providers=providers,
            knowledge_answer=rag_answer,
            citations=citations,
            observability_metrics=tracker.to_dict()
        )

coordinator_agent = PetCareCoordinatorAgent()
