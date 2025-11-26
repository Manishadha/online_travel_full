from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Account & Trips API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    account_id: str
    user_id: str


class CurrentUser(BaseModel):
    account_id: str
    user_id: str
    email: Optional[str] = None


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


class BookingCreate(BaseModel):
    journey_id: int
    passengers: int = 1


class Booking(BaseModel):
    id: int
    journey: Journey
    passengers: int
    total_price: float
    currency: str = "EUR"
    created_at: datetime


_FAKE_JOURNEYS: List[Journey] = [
    Journey(
        id=1,
        destination="Paris",
        title="Weekend in Paris",
        description="3 days in Paris with city tour and Seine river cruise.",
        start_date=date(2025, 3, 14),
        end_date=date(2025, 3, 16),
        is_group=False,
        max_people=4,
        price_per_person=320.0,
        currency="EUR",
    ),
    Journey(
        id=2,
        destination="New York",
        title="New York City Lights",
        description="5 nights in NYC with Broadway tickets included.",
        start_date=date(2025, 5, 1),
        end_date=date(2025, 5, 6),
        is_group=True,
        max_people=12,
        price_per_person=980.0,
        currency="EUR",
    ),
    Journey(
        id=3,
        destination="Rome",
        title="Rome & Vatican Discovery",
        description="Guided tours of the Colosseum and Vatican Museums.",
        start_date=date(2025, 4, 10),
        end_date=date(2025, 4, 14),
        is_group=True,
        max_people=20,
        price_per_person=650.0,
        currency="EUR",
    ),
]

_BOOKINGS: List[Booking] = []
_NEXT_BOOKING_ID: int = 1


@app.get("/health")
def health():
    return {"ok": True, "service": "account_api"}


@app.post("/v1/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    email = payload.email.strip().lower() or "demo@example.com"  # noqa: F841

    return LoginResponse(
        access_token="demo-015d614f-2810-49b1-ae1b-741daffe0030",
        account_id="2d90f602-d860-4c3c-9725-b71dbb0327bb",
        user_id="015d614f-2810-49b1-ae1b-741daffe0030",
    )


def get_current_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1].strip()
    if not token.startswith("demo-"):
        raise HTTPException(status_code=401, detail="Invalid token")

    return CurrentUser(
        account_id="2d90f602-d860-4c3c-9725-b71dbb0327bb",
        user_id="015d614f-2810-49b1-ae1b-741daffe0030",
        email="mani@example.com",
    )


@app.get("/v1/journeys", response_model=List[Journey])
def list_journeys(
    destination: Optional[str] = None,
    group_only: bool = False,
    max_price: Optional[float] = None,
    current_user: CurrentUser = Depends(get_current_user),
):
    items = _FAKE_JOURNEYS

    if destination:
        d = destination.lower()
        items = [j for j in items if d in j.destination.lower()]

    if group_only:
        items = [j for j in items if j.is_group]

    if max_price is not None:
        items = [j for j in items if j.price_per_person <= max_price]

    return items


@app.post("/v1/bookings", response_model=Booking)
def create_booking(
    payload: BookingCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    global _NEXT_BOOKING_ID

    journey = next((j for j in _FAKE_JOURNEYS if j.id == payload.journey_id), None)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    passengers = max(1, payload.passengers)
    total_price = journey.price_per_person * passengers

    booking = Booking(
        id=_NEXT_BOOKING_ID,
        journey=journey,
        passengers=passengers,
        total_price=total_price,
        currency=journey.currency,
        created_at=datetime.utcnow(),
    )
    _BOOKINGS.append(booking)
    _NEXT_BOOKING_ID += 1

    return booking


@app.get("/v1/bookings", response_model=List[Booking])
def list_bookings(
    current_user: CurrentUser = Depends(get_current_user),
):
    return _BOOKINGS
