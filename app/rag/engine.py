import json
import os
from typing import List, Dict, Any, Optional
from app.mcp.schemas import RAGSourceCitation

KNOWLEDGE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge", "indian_animal_care.json")

POLITE_DENIAL_FALLBACK = (
    "I do not have verified veterinary medical recommendations for this specific query in my official guidelines database. "
    "To ensure the safety, proper diagnosis, and health of your animal, please consult a licensed veterinarian directly "
    "at one of the nearby verified veterinary hospitals listed below for professional medical evaluation."
)

class RAGEngine:
    """Vertex AI RAG simulation & Local Knowledge Base Retriever with metadata filtering and polite denial fallback."""

    def __init__(self):
        self.corpus: List[Dict[str, Any]] = []
        self._load_corpus()

    def _load_corpus(self):
        try:
            if os.path.exists(KNOWLEDGE_FILE_PATH):
                with open(KNOWLEDGE_FILE_PATH, "r", encoding="utf-8") as f:
                    self.corpus = json.load(f)
        except Exception:
            self.corpus = []

    def search_knowledge(
        self,
        query: str,
        animal_type: Optional[str] = None,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        
        q_lower = query.lower()
        results: List[Dict[str, Any]] = []
        citations: List[RAGSourceCitation] = []

        # Ignore generic search query terms
        meaningful_words = [w for w in q_lower.split() if len(w) > 3 and w not in ["find", "near", "hospital", "clinic", "doctor", "where", "what", "which", "available"]]

        for doc in self.corpus:
            metadata = doc.get("metadata", {})
            doc_animal = metadata.get("animal_type", "").lower()
            doc_text = (doc.get("title", "") + " " + doc.get("content", "")).lower()

            # Animal type metadata filter
            if animal_type and animal_type.lower() != "other" and animal_type.lower() not in doc_animal:
                continue

            # Query keyword relevance score
            match_score = sum(1 for w in meaningful_words if w in doc_text)

            if match_score >= 1:
                results.append(doc)
                citations.append(
                    RAGSourceCitation(
                        title=doc.get("title", "Animal Care Guide"),
                        organization=metadata.get("authority", "Veterinary Authority"),
                        reference=f"{metadata.get('source', 'Veterinary Manual')} ({metadata.get('source_date', '2025')})",
                        animal_type=metadata.get("animal_type"),
                        severity=metadata.get("severity")
                    )
                )

        if results:
            content_snippets = "\n\n".join([f"[{d['title']}]: {d['content']}" for d in results])
        else:
            content_snippets = POLITE_DENIAL_FALLBACK

        return {
            "query": query,
            "results_count": len(results),
            "content": content_snippets,
            "citations": [c.dict() for c in citations]
        }

rag_engine = RAGEngine()
