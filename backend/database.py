import sqlite3
import json
import os
from datetime import datetime
from models import IncidentEvent

class Database:
    """
    Dedicated Data Access Layer (DAL).
    Uses SQLite (Standard Library) for zero-dependency persistence.
    """
    def __init__(self, db_path="events.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        # check_same_thread=False allows FastAPI to use the connection across requests
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row # Return dict-like rows
        return conn

    def _init_db(self):
        """Creates the schema on startup."""
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT,
                location TEXT,
                incident_type TEXT,
                severity TEXT,
                description TEXT,
                confidence REAL,
                duration_pred REAL,
                duration_uncertainty REAL,
                video_url TEXT,
                image_url TEXT
            )
        """)
        conn.commit()
        conn.close()

    def seed(self, json_path):
        """Populates DB if empty."""
        if not os.path.exists(json_path):
            return

        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Check if we have data
        cursor.execute("SELECT count(*) FROM events")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return # Already seeded

        print("⚡ Seeding Database from JSON...")
        with open(json_path, "r") as f:
            raw_data = json.load(f)
            
        for item in raw_data:
            # Normalize data using Pydantic
            evt = IncidentEvent(**item)
            
            # Insert using named placeholders (Safe from Injection)
            cursor.execute("""
                INSERT INTO events VALUES (
                    :event_id, :timestamp, :location, :incident_type, :severity, 
                    :description, :confidence, :duration_pred, :duration_uncertainty, 
                    :video_url, :image_url
                )
            """, evt.model_dump(by_alias=False))
            
        conn.commit()
        conn.close()
        print(f"✅ Seeded {len(raw_data)} events.")

    def add(self, event: IncidentEvent):
        conn = self._get_connection()
        try:
            conn.execute("""
                INSERT INTO events VALUES (
                    :event_id, :timestamp, :location, :incident_type, :severity, 
                    :description, :confidence, :duration_pred, :duration_uncertainty, 
                    :video_url, :image_url
                )
            """, event.model_dump(by_alias=False))
            conn.commit()
        finally:
            conn.close()

    def query(self, severity=None, incident_type=None, sort_by="timestamp"):
        conn = self._get_connection()
        
        # 1. Dynamic SQL Generation
        sql = "SELECT * FROM events"
        params = []
        filters = []
        
        if severity:
            filters.append("severity = ?")
            params.append(severity)
        if incident_type:
            filters.append("incident_type = ?")
            params.append(incident_type)
            
        if filters:
            sql += " WHERE " + " AND ".join(filters)
            
        # 2. Sorting Strategy
        sort_map = {
            "timestamp": "timestamp DESC",
            "confidence": "confidence DESC",
            "severity": "CASE severity WHEN 'high' THEN 3 WHEN 'medium' THEN 2 ELSE 1 END DESC"
        }
        sql += f" ORDER BY {sort_map.get(sort_by, 'timestamp DESC')}"
        
        # 3. Fetch & Hydrate
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [IncidentEvent(**dict(r)) for r in rows]

    def get_latest(self):
        res = self.query(sort_by="timestamp")
        return res[0] if res else None
        