import asyncio
import json
import time
from app.adk.agent import coordinator_agent

DEMO_SCENARIOS = [
    {"num": 1, "query": "Find a veterinary hospital near me for my dog.", "animal": "Dog"},
    {"num": 2, "query": "My dog is bleeding badly. Find an emergency vet.", "animal": "Dog"},
    {"num": 3, "query": "Find a 24/7 veterinary hospital.", "animal": "Dog"},
    {"num": 4, "query": "Find a government veterinary hospital for my buffalo.", "animal": "Buffalo"},
    {"num": 5, "query": "My bird is injured. Find an avian veterinarian.", "animal": "Bird"},
    {"num": 6, "query": "Find a pet pharmacy near me.", "animal": "Dog"},
    {"num": 7, "query": "Na kukka vomiting avutundi. Na daggara vet hospital kavali.", "animal": "Dog"},
    {"num": 8, "query": "నా గేదె తినడం లేదు. దగ్గరలో పశువైద్యశాల ఉందా?", "animal": "Buffalo"},
    {"num": 9, "query": "Find veterinary diagnostics near me.", "animal": "Dog"},
    {"num": 10, "query": "What should I do if my dog has repeated vomiting?", "animal": "Dog"}
]

async def execute_demo_scenarios():
    print("=" * 80)
    print("PETCARE INDIA AI - AUTOMATED DEMO SCENARIOS EXECUTION")
    print("=" * 80)

    for scenario in DEMO_SCENARIOS:
        print(f"\n--- DEMO {scenario['num']}: \"{scenario['query']}\" ---")
        t0 = time.time()
        
        resp = await coordinator_agent.process_user_request(
            query=scenario["query"],
            animal=scenario["animal"]
        )
        
        lat_ms = (time.time() - t0) * 1000.0

        print(f"• User Intent Detected  : Species: {resp.animal_detected} | Language: {resp.language} | Urgency: {resp.urgency_level}")
        print(f"• Agent Chain Selected : {' -> '.join(resp.agent_chain)}")
        print(f"• Tools Invoked        : {resp.observability_metrics.get('tools_invoked', [])}")
        print(f"• Retrieved Providers  : {len(resp.providers)} facility record(s)")
        if resp.providers:
            top = resp.providers[0]
            print(f"  └ Top Facility       : {top.name} ({top.distance_km} km away, Phone: {top.phone})")
        
        if resp.knowledge_answer:
            print(f"• RAG Answer Summary   : {resp.knowledge_answer[:120]}...")
        
        if resp.citations:
            print(f"• Citations Exposed    : {[c.title for c in resp.citations]}")
        
        print(f"• Safety Classification: Emergency Triggered = {resp.is_emergency}")
        print(f"• Total Latency        : {round(lat_ms, 2)} ms")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(execute_demo_scenarios())
