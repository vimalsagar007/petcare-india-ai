from app.safety.guardrails import safety_guardrails

def test_enforce_medical_safety():
    unsafe_text = "Your animal definitely has Parvovirus. This medicine will cure it 100%."
    safe_text = safety_guardrails.enforce_medical_safety(unsafe_text)
    assert "definitely" not in safe_text.lower()
    assert "Possible causes include" in safe_text
    assert "Disclaimer" in safe_text
