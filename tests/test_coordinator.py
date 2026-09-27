import pytest
from app.adk.agent import coordinator_agent

@pytest.mark.asyncio
async def test_coordinator_dog_hospital():
    resp = await coordinator_agent.process_user_request("Find a veterinary hospital near me for my dog.")
    assert resp.animal_detected == "Dog"
    assert len(resp.providers) > 0
    assert "DogVeterinaryAgent" in resp.agent_chain or "LocationDiscoveryAgent" in resp.agent_chain
