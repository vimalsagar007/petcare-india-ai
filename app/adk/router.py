import re
from typing import Dict, Any, Tuple, Optional
from app.maps.routes_client import routes_client

class RouterLogic:
    """Intent classifier, entity extractor, species detector, and agent router."""

    SPECIES_MAP = {
        "dog": "Dog", "kukka": "Dog", "kutta": "Dog", "naayi": "Dog", "patti": "Dog", "puppy": "Dog",
        "cat": "Cat", "pilli": "Cat", "billi": "Cat", "poochha": "Cat",
        "bird": "Bird", "pakshi": "Bird", "parinda": "Bird", "pitta": "Bird", "parrot": "Bird",
        "cow": "Cow", "aavu": "Cow", "gai": "Cow", "pasu": "Cow", "cattle": "Cow",
        "buffalo": "Buffalo", "gedhe": "Buffalo", "bhains": "Buffalo", "eruma": "Buffalo", "pashu": "Buffalo",
        "goat": "Goat", "meka": "Goat", "bakra": "Goat", "aadu": "Goat",
        "sheep": "Sheep", "gorre": "Sheep", "bhed": "Sheep",
        "horse": "Horse", "gurram": "Horse", "ghoda": "Horse",
        "rabbit": "Rabbit", "kundelu": "Rabbit", "khargosh": "Rabbit",
        "poultry": "Poultry", "kodi": "Poultry", "murgi": "Poultry", "chicken": "Poultry"
    }

    INDIAN_LANG_MAP = {
        "na ": "Telugu", "kukka": "Telugu", "avu": "Telugu", "gedhe": "Telugu", "kavali": "Telugu", "daggara": "Telugu", "avutundi": "Telugu", "లేదు": "Telugu", "ఉందా": "Telugu",
        "mera": "Hindi", "meri": "Hindi", "kutta": "Hindi", "bhaians": "Hindi", "chahiye": "Hindi", "paas": "Hindi",
        "yen": "Tamil", "nammal": "Malayalam", "nanna": "Kannada"
    }

    def parse_query(self, query: str, provided_animal: Optional[str] = None, provided_location: Optional[str] = None) -> Dict[str, Any]:
        q_lower = query.lower()

        # Detect language
        detected_lang = "English"
        for keyword, lang in self.INDIAN_LANG_MAP.items():
            if keyword in q_lower or any('\u0c00' <= char <= '\u0c7f' for char in query): # Telugu unicode range
                detected_lang = lang
                break

        # Detect animal
        animal = provided_animal if (provided_animal and provided_animal != "Other") else "Other"
        if animal == "Other":
            for k, v in self.SPECIES_MAP.items():
                if k in q_lower:
                    animal = v
                    break
        if animal == "Other":
            animal = "Dog" # Default fallback for general queries

        # Detect urgency & emergency
        is_emergency = any(w in q_lower for w in ["emergency", "bleeding", "accident", "hit by car", "collapsed", "dying", "urgent", "vomiting blood"])
        urgency = "Emergency" if is_emergency else ("Urgent" if "vomiting" in q_lower or "fever" in q_lower or "eating" in q_lower else "Normal")

        # Detect service required
        category = "all"
        if "government" in q_lower or "govt" in q_lower or "pashu chikitsalayam" in q_lower or "dispensary" in q_lower:
            category = "government"
        elif "emergency" in q_lower or is_emergency or "24/7" in q_lower or "24 hours" in q_lower:
            category = "emergency"
        elif animal in ["Cow", "Buffalo", "Goat", "Sheep", "Horse", "Poultry"]:
            category = "large_animal"
        elif animal == "Bird":
            category = "avian"
        elif "pharmacy" in q_lower or "medicine" in q_lower or "aushadhalaya" in q_lower:
            category = "pharmacy"
        elif "diagnostic" in q_lower or "lab" in q_lower or "scan" in q_lower:
            category = "diagnostics"
        elif "ambulance" in q_lower:
            category = "ambulance"

        # Detect location
        coords = routes_client.geocode_location(provided_location or query)

        # Decide routing requirements
        needs_maps = True
        needs_rag = any(w in q_lower for w in ["what should i do", "how to treat", "vaccination", "symptom", "care", "eating", "feed", "first aid", "why"]) or (not any(w in q_lower for w in ["find", "near", "hospital", "clinic", "doctor", "where"]))

        return {
            "query": query,
            "language": detected_lang,
            "animal": animal,
            "urgency": urgency,
            "is_emergency": is_emergency,
            "category": category,
            "latitude": coords[0],
            "longitude": coords[1],
            "needs_maps": needs_maps,
            "needs_rag": needs_rag
        }

router_logic = RouterLogic()
