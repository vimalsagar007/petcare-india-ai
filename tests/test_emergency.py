import pytest
from app.adk.agent import coordinator_agent

@pytest.mark.asyncio
async def test_emergency_workflow():
    resp = await coordinator_agent.process_user_request("My dog was hit by a car and is bleeding badly. Find an emergency vet.")
    assert resp.is_emergency is True
    assert resp.emergency_warning is not None
    assert "EmergencyVeterinaryAgent" in resp.agent_chain
    assert len(resp.providers) > 0
