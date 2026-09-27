import pytest
from app.adk.agent import coordinator_agent

@pytest.mark.asyncio
async def test_telugu_query_parsing():
    resp = await coordinator_agent.process_user_request("Na kukka vomiting avutundi. Na daggara vet hospital kavali.")
    assert resp.language in ["Telugu", "English"]
    assert resp.animal_detected == "Dog"
    assert len(resp.providers) > 0

@pytest.mark.asyncio
async def test_telugu_script_query():
    resp = await coordinator_agent.process_user_request("నా గేదె తినడం లేదు. దగ్గరలో పశువైద్యశాల ఉందా?")
    assert resp.language == "Telugu"
    assert resp.animal_detected == "Buffalo"
    assert len(resp.providers) > 0
