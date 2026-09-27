import re
from typing import Tuple, Optional

EMERGENCY_KEYWORDS = [
    "bleeding", "hit by car", "accident", "trauma", "unconscious",
    "collapsed", "breathing difficulty", "cannot breathe", "seizure",
    "poison", "bloat", "swelling", "vomiting blood", "labor emergency",
    "unable to stand", "choking", "snake bite", "dog bite"
]

FORBIDDEN_PHRASES = [
    "definitely has", "your animal definitely", "this medicine will cure",
    "give this prescription", "i diagnose", "guaranteed cure"
]

SAFE_PHRASINGS = {
    "definitely has": "Possible causes include",
    "this medicine will cure": "Veterinary treatment may involve",
    "give this prescription": "A veterinarian should evaluate and prescribe"
}

class SafetyGuardrails:
    """Medical safety guardrails and triage classifier for animal care."""

    def check_emergency(self, query: str) -> Tuple[bool, Optional[str]]:
        q_lower = query.lower()
        for kw in EMERGENCY_KEYWORDS:
            if kw in q_lower:
                warning = (
                    "EMERGENCY WARNING: Severe symptoms detected. "
                    "This application is not a substitute for professional veterinary care. "
                    "Please seek immediate evaluation at the nearest 24/7 veterinary hospital or animal emergency clinic."
                )
                return True, warning
        return False, None

    def enforce_medical_safety(self, text: str) -> str:
        """Sanitizes text output to ensure non-diagnostic language."""
        sanitized = text
        for forbidden, replacement in SAFE_PHRASINGS.items():
            pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
            sanitized = pattern.sub(replacement, sanitized)

        # Enforce obligatory veterinary disclaimer if medical advice is present
        if "cause" in sanitized.lower() or "symptom" in sanitized.lower() or "treatment" in sanitized.lower():
            if "veterinarian should evaluate" not in sanitized.lower():
                sanitized += "\n\n*Disclaimer: This information is for educational guidance only. A licensed veterinarian should evaluate your animal for diagnosis and treatment.*"
        
        return sanitized

safety_guardrails = SafetyGuardrails()
