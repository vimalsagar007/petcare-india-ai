from typing import Dict, Any, Optional
from app.mcp.tools import mcp_tools
from app.safety.guardrails import safety_guardrails
from app.a2a.messaging import a2a_bus

class VeterinaryRAGAgent:
    """Agent #8: VeterinaryRAGAgent - Source-grounded RAG retriever for general animal care."""

    async def execute(self, query: str, animal_type: Optional[str] = None) -> Dict[str, Any]:
        a2a_bus.dispatch("CoordinatorAgent", "VeterinaryRAGAgent", "REQUEST", {"query": query, "animal": animal_type})
        
        raw_rag = await mcp_tools.search_veterinary_knowledge(query, animal_type)
        sanitized_content = safety_guardrails.enforce_medical_safety(raw_rag.get("content", ""))

        response = {
            "query": query,
            "answer": sanitized_content,
            "citations": raw_rag.get("citations", [])
        }
        a2a_bus.dispatch("VeterinaryRAGAgent", "CoordinatorAgent", "RESPONSE", {"citations_count": len(raw_rag.get("citations", []))})
        return response

rag_vet_agent = VeterinaryRAGAgent()
