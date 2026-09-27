from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LocationCoordinates(BaseModel):
    latitude: float
    longitude: float

class ProviderRecord(BaseModel):
    place_id: str
    name: str
    address: str
    phone: Optional[str] = None
    location: LocationCoordinates
    distance_km: float = 0.0
    open_now: Optional[bool] = None
    opening_hours: List[str] = Field(default_factory=list)
    rating: Optional[float] = None
    review_count: Optional[int] = None
    types: List[str] = Field(default_factory=list)
    emergency_available: Optional[bool] = None
    animal_specialties: List[str] = Field(default_factory=list)
    provider_category: str = "Private Clinic" # Private Clinic, Government Hospital, Diagnostic, Pharmacy, Ambulance
    photo_url: Optional[str] = None
    maps_url: Optional[str] = None
    source: str = "Google Places"

class RAGSourceCitation(BaseModel):
    title: str
    organization: str
    reference: str
    animal_type: Optional[str] = None
    severity: Optional[str] = None

class AgentResponse(BaseModel):
    request_id: str
    session_id: str
    user_query: str
    language: str
    animal_detected: str
    urgency_level: str
    agent_chain: List[str]
    is_emergency: bool = False
    emergency_warning: Optional[str] = None
    providers: List[ProviderRecord] = Field(default_factory=list)
    knowledge_answer: Optional[str] = None
    citations: List[RAGSourceCitation] = Field(default_factory=list)
    observability_metrics: Dict[str, Any] = Field(default_factory=dict)
