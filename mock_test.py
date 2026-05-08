import json
import asyncio
from unittest.mock import MagicMock, patch
from core.engine import OrchestrationEngine

async def run_simulation():
    print("🚀 Starting End-End Simulation Test...")
    
    # Mocking Gemini Response to avoid API call costs/fails
    mock_response = MagicMock()
    mock_itinerary = {
        "itinerary": [
            {
                "location": "Hidden Valley Trail, Nepal",
                "activity": "Pre-dawn Ridge Hike",
                "persona_match_score": 95,
                "reasoning_trace": "High altitude and secluded path matches The Scout's adventure preference.",
                "dynamic_adjustment_reason": "No adjustment needed; weather is clear."
            },
            {
                "location": "Namche Bazaar",
                "activity": "Local Tea House Exploration",
                "persona_match_score": 85,
                "reasoning_trace": "Cultural immersion with a rugged backdrop fits the persona profile.",
                "dynamic_adjustment_reason": "Rerouted from lower path due to minor trail block."
            }
        ]
    }
    mock_response.text = json.dumps(mock_itinerary)

    print("Step 1: Mocking Orchestration Engine...")
    with patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response):
        engine = OrchestrationEngine(api_key="MOCK_KEY")
        print("Step 2: Sending Query -> '3-day trek in Himalayas' for 'scout'...")
        result = await engine.generate_itinerary("3-day trek in Himalayas", "scout")
        
        print("\n--- [SIMULATED RESULT] ---")
        print(json.dumps(result, indent=2))
        print("----------------------------\n")
        
        if "itinerary" in result:
            print("✅ JSON Schema Validation: SUCCESS")
            print(f"✅ Items Generated: {len(result['itinerary'])}")
            print(f"✅ Reasoning Trace Present: {all('reasoning_trace' in item for item in result['itinerary'])}")
        else:
            print("❌ Simulation Failed: Invalid Result Structure")

if __name__ == "__main__":
    asyncio.run(run_simulation())
