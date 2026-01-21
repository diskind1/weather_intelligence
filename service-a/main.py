from fastapi import FastAPI
from api_extractor import ingest_weather_for_location
from fastapi.encoders import jsonable_encoder
import requests

app = FastAPI(title="Service A - Ingestion")

@app.post("/ingest")
def read_external_data():
    data = ingest_weather_for_location("London")
    json_data = jsonable_encoder(data)

    url = "http://127.0.0.1:8002/clean"
    response = requests.post(url, json=json_data)



    return response.json

