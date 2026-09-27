import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from app.config import settings
from app.adk.agent import coordinator_agent
from app.adk.state import session_state, PetProfile
from app.evaluation.runner import EvaluationRunner

app = FastAPI(
    title=settings.app_name,
    description=settings.subtitle,
    version=settings.version
)

# Serve static files
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class SearchRequest(BaseModel):
    query: str
    animal: Optional[str] = "Dog"
    location: Optional[str] = "Hyderabad"
    radius_km: Optional[float] = 10.0
    urgency: Optional[str] = "Normal"
    language: Optional[str] = "English"

class ChatRequest(BaseModel):
    query: str
    animal: Optional[str] = "Dog"
    language: Optional[str] = "English"

@app.get("/")
async def get_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "PetCare India AI Server Running."}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.application_env,
        "google_cloud_project": settings.google_cloud_project
    }

@app.post("/api/search")
async def search_veterinary_providers(req: SearchRequest):
    try:
        response = await coordinator_agent.process_user_request(
            query=req.query,
            animal=req.animal,
            location_text=req.location,
            radius_km=req.radius_km or 10.0,
            urgency=req.urgency,
            language=req.language
        )
        return response.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def veterinary_chat(req: ChatRequest):
    try:
        response = await coordinator_agent.process_user_request(
            query=req.query,
            animal=req.animal,
            language=req.language
        )
        return response.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pets")
async def get_my_pets():
    return [p.dict() for p in session_state.get_user_pets()]

@app.post("/api/pets")
async def add_my_pet(pet: PetProfile):
    return session_state.add_pet(pet).dict()

@app.get("/api/eval")
async def run_evaluations():
    metrics = await EvaluationRunner.run_evaluation()
    return metrics

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=False)
