import json
import os
from typing import List, Dict, Any, Optional
from app.mcp.schemas import RAGSourceCitation

KNOWLEDGE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge", "indian_animal_care.json")

class RAGEngine:
    """Vertex AI RAG simulation & Local Knowledge Base Retriever with metadata filtering."""

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

        for doc in self.corpus:
            metadata = doc.get("metadata", {})
            doc_animal = metadata.get("animal_type", "").lower()
            doc_topic = metadata.get("topic", "").lower()
            doc_text = (doc.get("title", "") + " " + doc.get("content", "")).lower()

            # Metadata filter check
            if animal_type and animal_type.lower() != "other" and animal_type.lower() not in doc_animal:
                continue

            # Query keyword relevance score
            words = q_lower.split()
            match_score = sum(1 for w in words if len(w) > 3 and w in doc_text)

            if match_score > 0 or not words:
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

        # Fallback if specific animal filter returned no results, search entire corpus
        if not results and animal_type:
            for doc in self.corpus:
                metadata = doc.get("metadata", {})
                doc_text = (doc.get("title", "") + " " + doc.get("content", "")).lower()
                words = q_lower.split()
                if any(w in doc_text for w in words if len(w) > 3):
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

        content_snippets = "\n\n".join([f"[{d['title']}]: {d['content']}" for d in results]) if results else "No specific knowledge base article matched the query."
        
        return {
            "query": query,
            "results_count": len(results),
            "content": content_snippets,
            "citations": [c.dict() for c in citations]
        }

rag_engine = RAGEngine()
