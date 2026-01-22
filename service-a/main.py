from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import requests
import os
import time

from api_extractor import ingest_weather_for_location

app = FastAPI(title="Service A - Ingestion")

LOCATIONS = ["London", "Tel Aviv", "Jerusalem"]
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8000/clean")


def fetch_with_retries(location: str, retries: int = 4, delay: float = 1.5):
    """
    מנסה למשוך נתונים עבור location מספר פעמים.
    שימושי כשיש תקלת SSL/רשת רגעית.
    """
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            return ingest_weather_for_location(location)
        except Exception as e:
            last_err = e
            # השהייה קטנה עם backoff
            time.sleep(delay * attempt)

    # נכשל אחרי כל הניסיונות
    raise last_err


@app.post("/ingest")
def ingest():
    all_records = []
    failed = []

    for loc in LOCATIONS:
        try:
            records = fetch_with_retries(loc)
            all_records.extend(records)
        except Exception as e:
            failed.append({"location": loc, "error": str(e)})

    # אם שום מיקום לא הצליח
    if not all_records:
        raise HTTPException(
            status_code=502,
            detail={"msg": "No data fetched from external API", "failed": failed},
        )

    payload = jsonable_encoder(all_records)

    try:
        r = requests.post(SERVICE_B_URL, json=payload, timeout=60)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=r.text)

        out = r.json()
        if failed:
            out["failed_locations"] = failed
        return out

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
