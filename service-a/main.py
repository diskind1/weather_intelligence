from api_extractor import ingest_weather_for_location
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Service A - Ingestion")

@app.post("/ingest")
def read_external_data():
    data = ingest_weather_for_location("London")

    url = "http://127.0.0.1:8002/clean"
    response = requests.post(url=url, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    return {"status:": response.status_code, "count": len(data), "data": response.json()}





