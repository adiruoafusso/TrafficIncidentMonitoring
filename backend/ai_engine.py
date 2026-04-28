import os
import random
import uuid
from datetime import datetime
from typing import List
from pydantic import ValidationError

from models import IncidentEvent 

class FakeAIEngine:
    def __init__(self, static_root="backend/static"):
        self.video_dir = os.path.join(static_root, "videos")
        self.image_dir = os.path.join(static_root, "images")
        self.incident_types = ["Collison", "Stalled Vehicle", "Pedestrian on Highway", "Debris", "Fire"]

    def _get_random_asset_pair(self):
        """Finds a matching video/image pair from the generated demo files."""
        videos = [f for f in os.listdir(self.video_dir) if f.endswith(".mp4")]
        if not videos:
            return None, None
        
        vid_name = random.choice(videos)
        # Match demo_01.mp4 to demo_01.jpg
        img_name = vid_name.replace(".mp4", ".jpg")
        
        return vid_name, img_name

    def predict(self) -> IncidentEvent:
        """
        Simulates an AI inference cycle. 
        Picks a demo asset and generates realistic metadata.
        """
        vid_name, img_name = self._get_random_asset_pair()
        
        if not vid_name:
            raise FileNotFoundError("No demo assets found. Run build_demo_assets first.")

        # Simulate AI "Logic"
        conf = random.uniform(0.82, 0.99)
        severity = "high" if conf > 0.92 else "medium" if conf > 0.88 else "low"
        
        # Create the event following your Pydantic schema
        event = IncidentEvent(
            event_id=str(uuid.uuid4())[:8],
            timestamp=datetime.utcnow(),
            location=random.choice(["Hwy 101 - Northbound", "Interstate 5 - Exit 12", "Main St & 5th"]),
            type=random.choice(self.incident_types),
            severity=severity,
            description=f"AI detected a potential {severity} severity incident involving a {random.choice(['truck', 'sedan', 'motorcycle'])}.",
            confidence=round(conf, 2),
            duration_pred=round(random.uniform(5.0, 45.0), 1),
            duration_uncertainty=round(random.uniform(0.5, 3.5), 2),
            video_url=f"/static/videos/{vid_name}",
            image_url=f"/static/images/{img_name}"
        )
        
        return event

# --- Example Usage ---
# engine = FakeAIEngine()
# try:
#     result_json = engine.predict().model_dump_json(by_alias=True, indent=4)
#     print(result_json)
# except Exception as e:
#     print(f"Error: {e}")
