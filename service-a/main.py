from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import requests

from api_extractor import ingest_weather_for_location

app = FastAPI(title="Service A - Ingestion")

LOCATIONS = ["London", "Tel Aviv", "Jerusalem"]
SERVICE_B_URL = "http://127.0.0.1:8002/clean"

@app.post("/ingest")
def ingest():
    all_records = []
    for loc in LOCATIONS:
        all_records.extend(ingest_weather_for_location(loc))

    payload = jsonable_encoder(all_records)

    try:
        r = requests.post(SERVICE_B_URL, json=payload, timeout=60)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=r.text)
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
