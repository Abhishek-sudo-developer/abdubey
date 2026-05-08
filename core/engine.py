import json
import google.generativeai as genai
from core.agents import TravelAgent

class OrchestrationEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Using the specific stable version gemini-1.5-flash-002 as requested
        self.model = genai.GenerativeModel('gemini-1.5-flash-002')

    async def generate_itinerary(self, user_query, persona):
        agent = TravelAgent(persona)
        
        # Load schema
        with open('itinerary_schema.json', 'r') as f:
            schema = f.read()

        full_prompt = f"""
        {agent.get_logic_prompt()}
        
        JSON Schema for output:
        {schema}
        
        User Request: {user_query}
        
        IMPORTANT: Respond ONLY with a valid JSON object matching the schema. No markdown, no pre-amble.
        """

        response = self.model.generate_content(full_prompt)
        text = response.text
        
        try:
            # More robust JSON extraction: find first '{' and last '}'
            start_index = text.find('{')
            end_index = text.rfind('}')
            if start_index == -1 or end_index == -1:
                raise ValueError("No JSON found in response")
                
            json_str = text[start_index:end_index+1]
            itinerary_data = json.loads(json_str)
            return itinerary_data
        except Exception as e:
            print(f"FAILED TO PARSE GEMINI RESPONSE: {text}")
            return {"error": str(e), "raw_text": text}
