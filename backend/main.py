import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Modular imports
from models import IncidentEvent
from database import Database
from ai_engine import FakeAIEngine

app = FastAPI(title="Traffic AI API", version="3.1")

# --- 1. CORS CONFIGURATION ---
# Vital for allowing your frontend (likely on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. STATIC ASSETS ---
# Mount the directory where your build_demo_assets script saved the clips
# This allows the frontend to access /static/videos/demo_01.mp4
static_path = "static"
if not os.path.exists(static_path):
    os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# --- 3. CORE SERVICES ---
# Initialize DB and Engine once at startup
db = Database("events.db")
# Ensure the engine looks in the same 'static' folder for its assets
engine = FakeAIEngine(static_root=static_path)

@app.on_event("startup")
def startup():
    """
    Ensure the DB is ready and optionally seed it with initial data.
    """
    if os.path.exists("simulation/data.json"):
        db.seed("simulation/data.json")

# --- 4. API ROUTES ---

@app.get("/api/simulate", response_model=IncidentEvent)
def simulate_new_event():
    """
    The 'Trigger': Generates a new AI prediction, saves it, and returns it.
    Use this route to simulate a real-time detection event.
    """
    try:
        # Generate prediction using the Fake Engine
        new_event = engine.predict()
        # Save to DB so it shows up in history/logs
        db.add(new_event)
        return new_event
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No demo video assets found. Run build_demo_assets first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events/current", response_model=IncidentEvent)
def get_current_event():
    """
    Live Dashboard Feed: Returns the most recent detection.
    """
    event = db.get_latest()
    if not event:
        # If the DB is empty, generate a simulation on the fly to avoid 404
        return simulate_new_event()
    return event

@app.get("/api/events", response_model=List[IncidentEvent])
def get_events(
    severity: Optional[str] = None,
    type: Optional[str] = None,
    sort_by: str = Query("timestamp", enum=["timestamp", "confidence", "severity"])
):
    """
    Event History: Search and filter through all past detections.
    """
    events = db.query(severity=severity, incident_type=type, sort_by=sort_by)
    return events

@app.post("/api/events", response_model=IncidentEvent, status_code=201)
def create_event(event: IncidentEvent):
    """
    Manual Ingestion: In case you want to send an event from an external script.
    """
    try:
        db.add(event)
        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
