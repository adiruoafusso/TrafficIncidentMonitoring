from fasthtml.common import *
import httpx
import os
from typing import List
from models import IncidentEvent

# CONFIG
BACKEND_INTERNAL_URL = os.getenv("API_URL", "http://backend:8000")
PUBLIC_MEDIA_URL = "http://localhost:8000" 

app, rt = fast_app(hdrs=(picolink, Script(src="https://cdn.tailwindcss.com")))

# --- COMPONENTS ---

def StatusBadge(level):
    colors = {
        "high": "bg-red-600 text-white animate-pulse", 
        "medium": "bg-orange-500 text-white", 
        "low": "bg-blue-500 text-white"
    }
    return Span(level.upper(), cls=f"px-3 py-1 rounded-full text-xs font-bold {colors.get(level, 'bg-gray-500')}")

def Dashboard(event: IncidentEvent):
    """The Live View (Top Section)."""
    return Div(
        # LEFT: Video
        Div(
            Video(
                src=f"{PUBLIC_MEDIA_URL}{event.video_url}",
                poster=f"{PUBLIC_MEDIA_URL}{event.image_url}",
                autoplay=True, muted=True, loop=True, 
                cls="w-full rounded-xl shadow-2xl border border-slate-700"
            ),
            Div(
                H2(event.incident_type, cls="text-3xl font-black text-white tracking-tighter"),
                StatusBadge(event.severity),
                cls="flex justify-between items-center mt-4"
            ),
            P(event.description, cls="text-slate-400 mt-2 italic text-sm"),
            cls="col-span-2"
        ),
        # RIGHT: Metrics
        Div(
            Div(
                H3("AI Confidence", cls="text-slate-400 text-xs uppercase tracking-widest mb-1"),
                P(event.display_confidence, cls="text-5xl font-mono font-bold text-green-400"),
                cls="bg-slate-800 p-6 rounded-xl border border-slate-700"
            ),
            Div(
                H3("Clearance Time", cls="text-slate-400 text-xs uppercase tracking-widest mb-1"),
                P(f"{event.duration_pred} min", cls="text-4xl font-mono font-bold text-white"),
                Div(Span("±"), Span(f"{event.duration_uncertainty} min variance", cls="text-orange-400 text-sm")),
                cls="bg-slate-800 p-6 rounded-xl border border-slate-700 mt-4"
            ),
            Div(
                H3("Live Metadata", cls="text-slate-600 text-xs uppercase"),
                P(event.location, cls="text-slate-300 font-bold text-sm"),
                P(event.timestamp.strftime("%H:%M:%S UTC"), cls="text-slate-500 text-xs font-mono"),
                cls="bg-slate-900/50 p-6 rounded-xl border border-slate-800 mt-4"
            ),
            cls="col-span-1 flex flex-col"
        ),
        id="dashboard-content",
        hx_get="/poll", hx_trigger="every 3s", hx_swap="outerHTML",
        cls="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl"
    )

def HistoryTable(events: List[IncidentEvent]):
    """The Log View (Bottom Section) - Demonstrates Sorting/Filtering."""
    rows = []
    for e in events:
        rows.append(Tr(
            Td(e.timestamp.strftime("%H:%M:%S"), cls="p-3 font-mono text-xs text-slate-500"),
            Td(e.incident_type, cls="p-3 font-bold text-white"),
            Td(StatusBadge(e.severity), cls="p-3"),
            Td(e.display_confidence, cls="p-3 font-mono text-green-400"),
            cls="border-b border-slate-800 hover:bg-slate-800/50"
        ))
    
    return Div(
        # Toolbar
        Div(
            H3("Event Log", cls="text-xl font-bold text-white"),
            Div(
                Button("Latest", hx_get="/log?sort_by=timestamp", hx_target="#history-list", cls="px-3 py-1 bg-slate-700 rounded text-xs hover:bg-slate-600 mr-2"),
                Button("Highest Confidence", hx_get="/log?sort_by=confidence", hx_target="#history-list", cls="px-3 py-1 bg-slate-700 rounded text-xs hover:bg-slate-600 mr-2"),
                Button("High Severity Only", hx_get="/log?severity=high", hx_target="#history-list", cls="px-3 py-1 bg-red-900/50 border border-red-800 rounded text-xs hover:bg-red-900"),
                cls="flex"
            ),
            cls="flex justify-between items-center mb-4"
        ),
        # Table
        Table(
            Thead(Tr(
                Th("Time", cls="text-left p-3 text-xs text-slate-500"),
                Th("Type", cls="text-left p-3 text-xs text-slate-500"),
                Th("Severity", cls="text-left p-3 text-xs text-slate-500"),
                Th("Conf.", cls="text-left p-3 text-xs text-slate-500"),
            )),
            Tbody(*rows),
            cls="w-full text-left"
        ),
        id="history-list",
        cls="mt-12 bg-slate-900/50 border border-slate-800 rounded-xl p-6 w-full max-w-5xl"
    )

# --- ROUTES ---

@rt("/poll")
async def get_poll():
    """Updates the Top Dashboard Section."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_INTERNAL_URL}/api/events/current")
            return Dashboard(IncidentEvent(**resp.json()))
        except:
            return Div("Connecting...", cls="text-yellow-500")

@rt("/log")
async def get_log(sort_by: str = "timestamp", severity: str = None):
    """Updates the Bottom History Section (Handles Filters)."""
    params = {"sort_by": sort_by}
    if severity:
        params["severity"] = severity
        
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_INTERNAL_URL}/api/events", params=params)
            events = [IncidentEvent(**e) for e in resp.json()][:10] # Limit to 10 rows
            return HistoryTable(events)
        except Exception as e:
            return Div(f"Log Unavailable: {e}", cls="text-red-500 mt-10")

@rt("/")
async def get():
    """Full Page Layout."""
    return Title("Traffic AI Guard"), Body(
        Div(
            Div(
                H1("🚦 V-JEPA GUARD", cls="text-xl font-bold text-white"),
                P("Live Inference Stream", cls="text-xs text-slate-400"),
                cls="flex justify-between items-center border-b border-slate-800 pb-4 mb-8"
            ),
            await get_poll(),
            # Load the history log immediately
            await get_log(), 
            cls="bg-slate-900 min-h-screen p-10 font-sans flex flex-col items-center"
        )
    )

serve()
