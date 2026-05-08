import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()

class GoogleServices:
    """Wrapper for Google Maps, Places, and Weather APIs."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None

    def get_places(self, query, persona_type):
        """Search for locations using Google Places API."""
        if not self.client:
            return [{"name": f"Mock Place for {persona_type}", "rating": 4.8, "address": "123 Mock Way"}]
        
        try:
            # bias towards high-rated spots for Epicure/Minimalist etc.
            result = self.client.places(query=query)
            places = []
            for p in result.get('results', [])[:5]:
                places.append({
                    "name": p.get('name'),
                    "rating": p.get('rating'),
                    "address": p.get('formatted_address'),
                    "place_id": p.get('place_id')
                })
            return places
        except Exception as e:
            return {"error": str(e)}

    def get_directions(self, origin, destination):
        """Calculate distance and duration using Distance Matrix API."""
        if not self.client:
            return {"distance": "1.2km", "duration": "5 mins", "status": "Clear Traffic"}
        
        try:
            matrix = self.client.distance_matrix(origin, destination, departure_time="now")
            elements = matrix['rows'][0]['elements'][0]
            return {
                "distance": elements.get('distance', {}).get('text'),
                "duration": elements.get('duration_in_traffic', elements.get('duration', {})).get('text'),
                "status": "Live Traffic Data"
            }
        except Exception as e:
            return {"error": str(e)}

    def get_weather_pivot(self, location):
        """Simple mock for weather (standard for hackathon unless key provided)."""
        # In a real app, we'd use OpenWeather or similar.
        return {"current": "Sunny", "forecast": "Clear", "reroute_needed": False}
