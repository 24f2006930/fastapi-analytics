import os
from collections import defaultdict
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

API_KEY = os.getenv("ANALYTICS_API_KEY", "ak_64ns35dz84qrf7nql9a5rpow")
EMAIL = os.getenv("STUDENT_EMAIL", "24f2006930@ds.study.iitm.ac.in")

app = FastAPI(title="Event Analytics API")

# The assignment allows wildcard CORS so the browser-based grader can call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event] = Field(default_factory=list)


@app.get("/")
async def root():
    return {"status": "ok", "endpoint": "/analytics", "method": "POST"}


@app.post("/analytics")
async def analytics(
    body: AnalyticsRequest,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    positive_totals: dict[str, float] = defaultdict(float)
    revenue = 0.0
    for event in body.events:
        if event.amount > 0:
            revenue += event.amount
            positive_totals[event.user] += event.amount

    top_user = max(positive_totals, key=positive_totals.get) if positive_totals else ""

    return {
        "email": EMAIL,
        "total_events": len(body.events),
        "unique_users": len({event.user for event in body.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
