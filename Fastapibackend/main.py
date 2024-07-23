from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
import mysql.connector

app = FastAPI()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="traveldb"
    )

# Models
class BookingRequest(BaseModel):
    user_id: int
    destination: str
    date: str
    type: str  # flight or hotel

@app.post("/book")
def book(request: BookingRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (user_id, destination, date, type) VALUES (%s, %s, %s, %s)",
        (request.user_id, request.destination, request.date, request.type)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Booking confirmed"}

@app.get("/destinations/{destination}")
def get_destination_info(destination: str):
    # Mock response for destination info
    return {"destination": destination, "info": "Popular tourist spot with beautiful beaches."}

@app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "book_flight":
        # Extract parameters
        user_id = req["queryResult"]["parameters"]["user_id"]
        destination = req["queryResult"]["parameters"]["geo-city"]
        date = req["queryResult"]["parameters"]["date"]

        # Call the book endpoint
        booking_request = BookingRequest(user_id=user_id, destination=destination, date=date, type="flight")
        book(booking_request)
        return {"fulfillmentText": "Your flight has been booked."}

    # Handle other intents similarly
    return {"fulfillmentText": "I didn't understand that."}
