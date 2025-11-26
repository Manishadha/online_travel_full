from __future__ import annotations

from datetime import date
from typing import Optional, List  # noqa: F401

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# -----------------------
# Models
# -----------------------
class Journey(BaseModel):
    id: int
    destination: str
    title: str
    description: str
    start_date: date
    end_date: date
    is_group: bool
    max_people: int
    price_per_person: float
    currency: str = "EUR"


# -----------------------
# App + CORS
# -----------------------
app = FastAPI(title="My Trips API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True, "service": "my_trips_api"}


# -----------------------
# Fake data
# -----------------------
def _fake_journeys() -> list[Journey]:
    return [
        Journey(
            id=1,
            destination="Paris",
            title="Weekend in Paris",
            description="3 days in Paris with city tour and Seine river cruise.",
            start_date=date(2025, 5, 16),
            end_date=date(2025, 5, 18),
            is_group=False,
            max_people=2,
            price_per_person=280.0,
        ),
        Journey(
            id=2,
            destination="New York",
            title="NYC Highlights (Group)",
            description="5-day group trip with Times Square, Brooklyn, and museums.",
            start_date=date(2025, 6, 2),
            end_date=date(2025, 6, 6),
            is_group=True,
            max_people=20,
            price_per_person=950.0,
        ),
        Journey(
            id=3,
            destination="Barcelona",
            title="Barcelona Beach & Culture",
            description="4 days between the beach, tapas, and Gaudí architecture.",
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 13),
            is_group=False,
            max_people=4,
            price_per_person=520.0,
        ),
        Journey(
            id=4,
            destination="Iceland",
            title="Iceland Adventure (Group)",
            description="7-day group tour: waterfalls, glaciers, and hot springs.",
            start_date=date(2025, 8, 3),
            end_date=date(2025, 8, 9),
            is_group=True,
            max_people=12,
            price_per_person=1850.0,
        ),
    ]


# -----------------------
# Journeys endpoint
# -----------------------
@app.get("/journeys", response_model=list[Journey])
def list_journeys(
    destination: Optional[str] = Query(
        None, description="Filter by destination (case-insensitive substring)"
    ),
    group_only: bool = Query(
        False, description="If true, only show group journeys"
    ),
    max_price: Optional[float] = Query(
        None, description="Maximum price per person"
    ),
):
    """
    Simple in-memory search.

    - Filter by destination substring
    - Filter to group trips only
    - Filter by max price per person
    """
    journeys = _fake_journeys()

    if destination:
        d = destination.lower()
        journeys = [j for j in journeys if d in j.destination.lower()]

    if group_only:
        journeys = [j for j in journeys if j.is_group]

    if max_price is not None:
        journeys = [j for j in journeys if j.price_per_person <= max_price]

    return journeys
