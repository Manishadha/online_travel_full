from __future__ import annotations

from datetime import date
from typing import List, Optional  # noqa: F401

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# -----------------------
# Models
# -----------------------
class Trip(BaseModel):
    id: int
    kind: str  # "flight" | "hotel"
    origin: str
    destination: str
    depart_date: date
    return_date: Optional[date] = None
    title: str
    description: str
    price: float
    currency: str = "EUR"
    airline: Optional[str] = None
    hotel_name: Optional[str] = None
    rating: Optional[float] = None


# class TripSearchResponse(BaseModel):
 #   items: List[Trip]


class BookingCreate(BaseModel):
    trip_id: int
    customer_name: str
    email: str
    passengers: int = 1


class Booking(BaseModel):
    id: int
    trip: Trip
    customer_name: str
    email: str
    passengers: int
    total_price: float
    currency: str = "EUR"


# -----------------------
# App + CORS
# -----------------------
app = FastAPI(title="Travel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True, "service": "travel_api"}


# -----------------------
# Fake data helpers
# -----------------------
def _fake_trips(origin: str, destination: str, travel_date: date, kind: str) -> list[Trip]:
    origin = origin.upper()
    destination = destination.upper()
    kind = kind.lower()

    results: list[Trip] = []

    if kind in {"both", "flight"}:
        results.append(
            Trip(
                id=1,
                kind="flight",
                origin=origin,
                destination=destination,
                depart_date=travel_date,
                title=f"{origin} → {destination} direct flight",
                description="Non-stop flight with 1 checked bag included.",
                price=320.0,
                currency="EUR",
                airline="Velu Air",
            )
        )

    if kind in {"both", "hotel"}:
        results.append(
            Trip(
                id=2,
                kind="hotel",
                origin=destination,
                destination=destination,
                depart_date=travel_date,
                title=f"3-night stay in {destination}",
                description="Modern 4★ hotel near city center, breakfast included.",
                price=210.0,
                currency="EUR",
                hotel_name="Hotel Velu Plaza",
                rating=4.4,
            )
        )

    return results


# -----------------------
# Search endpoint
# -----------------------

@app.get("/search/trips", response_model=list[Trip])
def search_trips(
    origin: str = Query(..., min_length=3, max_length=5),
    destination: str = Query(..., min_length=3, max_length=5),
    travel_date: date = Query(...),
    kind: str = Query("both"),
    max_price: Optional[float] = None,
):
    trips = _fake_trips(origin, destination, travel_date, kind)

    if max_price is not None:
        trips = [t for t in trips if t.price <= max_price]

    # 🔹 Just return the plain list
    return trips


# -----------------------
# Bookings (in-memory)
# -----------------------
BOOKINGS: list[Booking] = []
NEXT_BOOKING_ID: int = 1


@app.post("/bookings", response_model=Booking)
def create_booking(payload: BookingCreate):
    global NEXT_BOOKING_ID

    # For now we just regenerate the trips and find the one with this ID.
    # In a real app you'd store trips in a DB and look up by ID.
    trips = _fake_trips("BRU", "JFK", date.today(), "both")  # very naive lookup

    trip = next((t for t in trips if t.id == payload.trip_id), None)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    total_price = trip.price * max(1, payload.passengers)

    booking = Booking(
        id=NEXT_BOOKING_ID,
        trip=trip,
        customer_name=payload.customer_name,
        email=payload.email,
        passengers=max(1, payload.passengers),
        total_price=total_price,
        currency=trip.currency,
    )
    BOOKINGS.append(booking)
    NEXT_BOOKING_ID += 1
    return booking



@app.get("/bookings", response_model=list[Booking])
def list_bookings(email: Optional[str] = Query(None)) -> list[Booking]:
    """
    Return all bookings currently stored in memory.

    If `email` is provided, only return bookings for that email.
    """
    if email:
        email_lower = email.lower()
        return [b for b in BOOKINGS if b.email.lower() == email_lower]
    return list(BOOKINGS)