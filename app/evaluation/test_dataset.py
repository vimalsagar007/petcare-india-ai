from typing import List, Dict, Any

EVALUATION_DATASET: List[Dict[str, Any]] = [
    {
        "id": "eval_01",
        "name": "Nearby veterinary hospital",
        "query": "Find a veterinary hospital near me in Hyderabad for my dog.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "DogVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_02",
        "name": "Emergency veterinary hospital",
        "query": "My dog was hit by a car and is bleeding badly. Find an emergency vet.",
        "expected_animal": "Dog",
        "expected_category": "emergency",
        "expected_agent": "EmergencyVeterinaryAgent",
        "expected_emergency": True
    },
    {
        "id": "eval_03",
        "name": "Government veterinary hospital",
        "query": "Find a government veterinary hospital pashu chikitsalayam in Guntur.",
        "expected_animal": "Cow",
        "expected_category": "government",
        "expected_agent": "GovernmentVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_04",
        "name": "Dog specialist",
        "query": "Looking for a dog specialist clinic in Jubliee Hills Hyderabad.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "DogVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_05",
        "name": "Cat specialist",
        "query": "Find a cat vet near me for my cat's vaccination.",
        "expected_animal": "Cat",
        "expected_category": "all",
        "expected_agent": "CatVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_06",
        "name": "Avian veterinarian",
        "query": "My bird is injured. Find an avian veterinarian in Bengaluru.",
        "expected_animal": "Bird",
        "expected_category": "avian",
        "expected_agent": "AvianVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_07",
        "name": "Buffalo veterinarian",
        "query": "My buffalo is not eating fodder. Need a cattle veterinarian in Vijayawada.",
        "expected_animal": "Buffalo",
        "expected_category": "large_animal",
        "expected_agent": "LivestockVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_08",
        "name": "Cattle veterinarian",
        "query": "Find a Pashu Vaidya for my cow in Guntur.",
        "expected_animal": "Cow",
        "expected_category": "large_animal",
        "expected_agent": "LivestockVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_09",
        "name": "Closed hospital filter",
        "query": "Show veterinary hospitals currently open.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "LocationDiscoveryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_10",
        "name": "Open hospital",
        "query": "Find 24/7 animal hospital near Narayanguda Hyderabad.",
        "expected_animal": "Dog",
        "expected_category": "emergency",
        "expected_agent": "EmergencyVeterinaryAgent",
        "expected_emergency": True
    },
    {
        "id": "eval_11",
        "name": "No result fallback test",
        "query": "Find veterinary hospital in remote hamlet XYZ.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "LocationDiscoveryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_12",
        "name": "Expanding search radius",
        "query": "Search vet within 1 km in Warangal.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "LocationDiscoveryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_13",
        "name": "Incorrect location input",
        "query": "Find vet in InvalidCityName123.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "LocationDiscoveryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_14",
        "name": "Telugu query",
        "query": "నా గేదె తినడం లేదు. దగ్గరలో పశువైద్యశాల ఉందా?",
        "expected_animal": "Buffalo",
        "expected_category": "large_animal",
        "expected_agent": "LivestockVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_15",
        "name": "Hindi query",
        "query": "Mera kutta khana nahi kha raha, paas me pashu chikitsalaya batao.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "DogVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_16",
        "name": "Mixed-language query",
        "query": "Na kukka vomiting avutundi, nearby vet hospital kavali.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "DogVeterinaryAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_17",
        "name": "Emergency symptom triage",
        "query": "Dog collapsed and breathing difficulty.",
        "expected_animal": "Dog",
        "expected_category": "emergency",
        "expected_agent": "EmergencyVeterinaryAgent",
        "expected_emergency": True
    },
    {
        "id": "eval_18",
        "name": "Medical hallucination attempt",
        "query": "What medicine will 100% cure Parvovirus at home without vet?",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "VeterinaryRAGAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_19",
        "name": "Fake doctor request",
        "query": "Give me the phone number of Dr. John FakeDoctor123 in Hyderabad.",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "ProviderVerificationAgent",
        "expected_emergency": False
    },
    {
        "id": "eval_20",
        "name": "Fake hospital request",
        "query": "Is NonExistentHospitalX open today?",
        "expected_animal": "Dog",
        "expected_category": "all",
        "expected_agent": "ProviderVerificationAgent",
        "expected_emergency": False
    }
]
