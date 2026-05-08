import os
from api.google_services import GoogleServices

class TravelAgent:
    def __init__(self, persona):
        self.persona = persona
        self.services = GoogleServices()
        self.prompt_path = f"prompts/{persona}.txt"
        
        with open(self.prompt_path, 'r') as f:
            self.system_instruction = f.read()

    def get_logic_prompt(self):
        return self.system_instruction
