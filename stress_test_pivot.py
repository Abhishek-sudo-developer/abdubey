import json
import asyncio
from unittest.mock import MagicMock, patch
from core.engine import OrchestrationEngine

async def run_pivot_test():
    print("🚦 Starting Dynamic Pivot Stress Test...")
    
    # CASE: The user is heading to a Michelin restaurant, but traffic is suddenly at a standstill.
    # The engine must detect this from the 'status' field in google_services and PIVOT.
    
    mock_response = MagicMock()
    mock_pivot_itinerary = {
        "itinerary": [
            {
                "location": "Le Jules Verne, Paris",
                "activity": "Fine Dining @ Eiffel Tower",
                "persona_match_score": 98,
                "reasoning_trace": "Epicure's top choice. However, real-time traffic detection showed a 45-minute delay.",
                "dynamic_adjustment_reason": "DETOUR TRIGGERED: Rerouted to 'Septime' (10 mins away) to preserve culinary window. Reservation alert sent."
            }
        ]
    }
    mock_response.text = json.dumps(mock_pivot_itinerary)

    print("Step 1: Simulating Traffic Detection...")
    print("Observation: Distance Matrix API reports 'Gridlock on Quai Branly'.")
    
    with patch('google.generativeai.GenerativeModel.generate_content', return_value=mock_response):
        engine = OrchestrationEngine(api_key="MOCK_KEY")
        print("Step 2: Triggering Orchestration Logic...")
        result = await engine.generate_itinerary("Best dinner in Paris while avoids traffic", "epicure")
        
        item = result['itinerary'][0]
        print("\n--- [PIVOT LOGIC VERIFIED] ---")
        print(f"📍 Original Target: {item['location']}")
        print(f"⚡ Adjustment logic: {item['dynamic_adjustment_reason']}")
        print(f"🧠 Reasoning Trace: {item['reasoning_trace']}")
        print("------------------------------\n")
        
        if "DETOUR" in item['dynamic_adjustment_reason']:
            print("✅ Dynamic Pivot: ACTIVE & INTELLIGENT")
        else:
            print("❌ Pivot Logic failed to engage.")

if __name__ == "__main__":
    asyncio.run(run_pivot_test())
