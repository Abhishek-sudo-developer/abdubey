import json
import google.generativeai as genai
from core.agents import TravelAgent

class OrchestrationEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Using the state-of-the-art gemini-2.5-flash (2026 Stable Standard)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_itinerary(self, user_query, persona):
        agent = TravelAgent(persona)
        
        with open('itinerary_schema.json', 'r') as f:
            schema = f.read()

        # Phase 1: ReAct Loop for Tool Usage
        chat = self.model.start_chat(history=[])
        loop_prompt = f"""
        {agent.get_logic_prompt()}
        
        Available tools:
        - search_places(query)
        - get_trip_metrics(origin, destination)
        
        You operate in a ReAct loop: THOUGHT -> ACTION -> OBSERVATION.
        When you have the final data, output the FINAL ITINERARY in JSON matching this schema:
        {schema}
        
        User Request: {user_query}
        """

        response = chat.send_message(loop_prompt)
        text = response.text
        max_turns = 3
        
        for _ in range(max_turns):
            if "itinerary" in text.lower() and "{" in text:
                break
                
            # Basic Action Parsing: action: tool_name("args")
            if "action:" in text.lower():
                action_line = [l for l in text.split('\n') if "action:" in l.lower()][0]
                # Execute tool using the agent's services
                if "search_places" in action_line:
                    query = action_line.split('("')[1].split('")')[0]
                    obs = agent.services.get_places(query, persona)
                    response = chat.send_message(f"OBSERVATION: {obs}")
                    text = response.text
                elif "get_trip_metrics" in action_line:
                    # Parse args and call
                    response = chat.send_message(f"OBSERVATION: Tool call acknowledged.")
                    text = response.text
            else:
                break

        # Final JSON Extraction
        try:
            start_index = text.find('{')
            end_index = text.rfind('}')
            if start_index == -1: return {"error": "No JSON found", "raw": text}
            return json.loads(text[start_index:end_index+1])
        except Exception as e:
            return {"error": str(e), "raw_text": text}
