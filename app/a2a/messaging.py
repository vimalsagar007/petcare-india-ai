from typing import Dict, Any, List
from pydantic import BaseModel, Field
import time

class A2AMessage(BaseModel):
    sender: str
    recipient: str
    message_type: str  # REQUEST, RESPONSE, DELEGATE
    payload: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)

class A2ABus:
    """Agent-to-Agent (A2A) inter-agent communication bus."""

    def __init__(self):
        self.message_history: List[A2AMessage] = []

    def dispatch(self, sender: str, recipient: str, message_type: str, payload: Dict[str, Any]) -> A2AMessage:
        msg = A2AMessage(
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            payload=payload
        )
        self.message_history.append(msg)
        return msg

a2a_bus = A2ABus()
