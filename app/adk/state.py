from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PetProfile(BaseModel):
    id: str
    name: str
    animal_type: str  # Dog, Cat, Bird, Cow, Buffalo, Goat, Sheep, Horse, Rabbit, Poultry, Other
    breed: Optional[str] = "Mixed Breed"
    age: Optional[str] = "Unknown"
    sex: Optional[str] = "Unknown"
    vaccination_status: Optional[str] = "Up to date"
    allergies: Optional[str] = "None reported"
    notes: Optional[str] = ""

class SessionState:
    """Manages active user sessions and 'My Pets' animal profiles."""

    def __init__(self):
        # Default in-memory profile store initialized with sample data
        self.pets_store: Dict[str, List[PetProfile]] = {
            "default_user": [
                PetProfile(
                    id="pet_001",
                    name="Bruno",
                    animal_type="Dog",
                    breed="Labrador Retriever",
                    age="4 years",
                    sex="Male",
                    vaccination_status="Anti-Rabies & 7-in-1 complete (User supplied)",
                    allergies="Chicken protein sensitivity",
                    notes="Friendly family pet in Hyderabad"
                ),
                PetProfile(
                    id="pet_002",
                    name="Gauri",
                    animal_type="Buffalo",
                    breed="Murrah",
                    age="5 years",
                    sex="Female",
                    vaccination_status="FMD vaccinated (User supplied)",
                    allergies="None",
                    notes="High-yield dairy buffalo"
                )
            ]
        }

    def get_user_pets(self, user_id: str = "default_user") -> List[PetProfile]:
        return self.pets_store.get(user_id, [])

    def add_pet(self, pet: PetProfile, user_id: str = "default_user") -> PetProfile:
        if user_id not in self.pets_store:
            self.pets_store[user_id] = []
        self.pets_store[user_id].append(pet)
        return pet

    def delete_pet(self, pet_id: str, user_id: str = "default_user") -> bool:
        if user_id in self.pets_store:
            initial = len(self.pets_store[user_id])
            self.pets_store[user_id] = [p for p in self.pets_store[user_id] if p.id != pet_id]
            return len(self.pets_store[user_id]) < initial
        return False

session_state = SessionState()
