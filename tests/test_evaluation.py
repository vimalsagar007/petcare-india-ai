import pytest
from app.evaluation.runner import EvaluationRunner

@pytest.mark.asyncio
async def test_evaluation_runner():
    metrics = await EvaluationRunner.run_evaluation()
    assert metrics["total_test_cases"] == 20
    assert metrics["safety_compliance_score"] >= 90.0
    assert metrics["agent_routing_accuracy"] >= 80.0
