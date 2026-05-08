from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.engine import OrchestrationEngine
import os

app = FastAPI(title="Dynamic Travel Orchestrator")

class PlanRequest(BaseModel):
    user_request: str
    persona: str

@app.post("/api/plan")
async def generate_plan(request: PlanRequest):
    engine = OrchestrationEngine(os.getenv("GEMINI_API_KEY"))
    itinerary = await engine.generate_itinerary(request.user_request, request.persona)
    
    return {
        "itinerary": itinerary,
        "logs": [] # Logic logs can be integrated here later
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
