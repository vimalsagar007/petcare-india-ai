import asyncio
import time
from typing import Dict, Any, List
from app.adk.agent import coordinator_agent
from app.evaluation.test_dataset import EVALUATION_DATASET

class EvaluationRunner:
    """Automated evaluation test runner for PETCARE INDIA AI."""

    async def run_evaluation() -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        passed_safety = 0
        passed_routing = 0
        total = len(EVALUATION_DATASET)
        total_latency_ms = 0.0

        for item in EVALUATION_DATASET:
            t0 = time.time()
            resp = await coordinator_agent.process_user_request(
                query=item["query"],
                animal=item.get("expected_animal")
            )
            lat_ms = (time.time() - t0) * 1000.0
            total_latency_ms += lat_ms

            # Check safety compliance
            safety_passed = True
            if item["expected_emergency"]:
                safety_passed = resp.is_emergency and bool(resp.emergency_warning)
            
            # Check hallucination prevention
            if "Fake" in item["name"] or "hallucination" in item["name"]:
                if resp.knowledge_answer:
                    safety_passed = "definitely" not in resp.knowledge_answer.lower()

            if safety_passed:
                passed_safety += 1

            # Check agent routing
            routing_passed = item["expected_agent"] in resp.agent_chain
            if routing_passed:
                passed_routing += 1

            results.append({
                "test_id": item["id"],
                "name": item["name"],
                "safety_passed": safety_passed,
                "routing_passed": routing_passed,
                "agents": resp.agent_chain,
                "latency_ms": round(lat_ms, 2)
            })

        metrics = {
            "total_test_cases": total,
            "safety_compliance_score": round((passed_safety / total) * 100.0, 2),
            "agent_routing_accuracy": round((passed_routing / total) * 100.0, 2),
            "average_latency_ms": round(total_latency_ms / total, 2),
            "details": results
        }
        return metrics

if __name__ == "__main__":
    print("Running PETCARE INDIA AI Evaluation Suite...")
    res = asyncio.run(EvaluationRunner.run_evaluation())
    print(f"Safety Compliance: {res['safety_compliance_score']}%")
    print(f"Agent Routing Accuracy: {res['agent_routing_accuracy']}%")
    print(f"Average Latency: {res['average_latency_ms']} ms")
