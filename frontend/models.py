from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class IncidentEvent(BaseModel):
    """
    Shared Data Contract between Backend (API) and Frontend (UI).
    """
    # --- CONFIGURATION ---
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()} 
    )
    # --- FIELDS ---
    # 1. Identity & Time
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    location: str = "Unspecified Location"
    # 2. Classification
    incident_type: str = Field(alias="type")
    severity: str  # low, medium, high
    description: str = "No details provided."
    # 3. AI Metadata
    confidence: float
    duration_pred: float
    duration_uncertainty: float
    # 4. Media
    video_url: str
    image_url: str
    
    # --- HELPERS (View Model) ---
    @property
    def display_confidence(self) -> str:
        return f"{int(self.confidence * 100)}%"
