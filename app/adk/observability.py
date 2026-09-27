import time
import uuid
from typing import Dict, Any, List

class LatencyTracker:
    def __init__(self, request_id: str, session_id: str):
        self.request_id = request_id or str(uuid.uuid4())
        self.session_id = session_id or "session_default"
        self.start_time = time.time()
        self.agent_selected: List[str] = []
        self.tools_invoked: List[str] = []
        self.tool_latency_ms: float = 0.0
        self.gemini_latency_ms: float = 0.0
        self.rag_latency_ms: float = 0.0
        self.a2a_latency_ms: float = 0.0
        self.mcp_latency_ms: float = 0.0
        self.errors: List[str] = []
        self.fallbacks: List[str] = []

    def record_agent(self, name: str):
        if name not in self.agent_selected:
            self.agent_selected.append(name)

    def record_tool(self, tool_name: str, latency_ms: float):
        self.tools_invoked.append(tool_name)
        self.tool_latency_ms += latency_ms
        self.mcp_latency_ms += latency_ms

    def record_rag(self, latency_ms: float):
        self.rag_latency_ms += latency_ms

    def record_gemini(self, latency_ms: float):
        self.gemini_latency_ms += latency_ms

    def record_a2a(self, latency_ms: float):
        self.a2a_latency_ms += latency_ms

    def record_fallback(self, msg: str):
        self.fallbacks.append(msg)

    def to_dict(self) -> Dict[str, Any]:
        total_latency = (time.time() - self.start_time) * 1000.0
        return {
            "request_id": self.request_id,
            "session_id": self.session_id,
            "agent_selected": self.agent_selected,
            "tools_invoked": self.tools_invoked,
            "tool_latency_ms": round(self.tool_latency_ms, 2),
            "gemini_latency_ms": round(self.gemini_latency_ms, 2),
            "rag_latency_ms": round(self.rag_latency_ms, 2),
            "a2a_latency_ms": round(self.a2a_latency_ms, 2),
            "mcp_latency_ms": round(self.mcp_latency_ms, 2),
            "errors": self.errors,
            "fallbacks": self.fallbacks,
            "final_response_latency_ms": round(total_latency, 2)
        }
