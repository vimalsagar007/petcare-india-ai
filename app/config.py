import os
from typing import List, Dict
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "PETCARE INDIA AI"
    subtitle: str = "Find trusted veterinary care for every animal, anywhere in India."
    version: str = "1.0.0"
    
    # Cloud & API Config
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "petcare-india-ai-prod")
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "asia-south1")
    google_maps_api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    rag_corpus_id: str = os.getenv("RAG_CORPUS_ID", "petcare_india_rag_v1")
    application_env: str = os.getenv("APPLICATION_ENV", "development")
    port: int = int(os.getenv("PORT", "8000"))

    # Supported Animals
    supported_animals: List[str] = [
        "Dog", "Cat", "Bird", "Cow", "Buffalo", 
        "Goat", "Sheep", "Horse", "Rabbit", "Poultry", "Other"
    ]

    # Supported Languages
    supported_languages: List[str] = [
        "English", "Telugu", "Hindi", "Tamil", 
        "Kannada", "Malayalam", "Marathi", "Bengali"
    ]

    # Indian Terminology dictionary mapping for query expansion
    indian_terms: Dict[str, List[str]] = {
        "vet": ["Veterinary Doctor", "Veterinary Hospital", "Pashu Vaidya", "Pashu Hospital", "Pashu Chikitsalayam"],
        "government": ["Government Veterinary Hospital", "Veterinary Dispensary", "Animal Husbandry Facility", "Livestock Hospital", "Mobile Veterinary Unit"],
        "cattle": ["Cattle Vet", "Cow Doctor", "Pashu Chikitsaka", "Large Animal Vet"],
        "buffalo": ["Buffalo Vet", "Buff Doctor", "Pashu Chikitsaka", "Livestock Hospital"],
        "emergency": ["24 Hours Veterinary Hospital", "Emergency Animal Hospital", "Pet Emergency Care", "Urgent Animal Care"],
        "pharmacy": ["Pet Pharmacy", "Veterinary Medical Store", "Pashu Aushadhalaya"],
        "diagnostics": ["Veterinary Diagnostics", "Animal Diagnostic Center", "Pet Scan Center", "Veterinary Lab"],
        "ambulance": ["Animal Ambulance", "Pet Ambulance Service", "Pashu Ambulance"]
    }

settings = Settings()
