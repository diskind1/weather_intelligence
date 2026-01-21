from fastapi import FastAPI
from api_extractor import ingest_weather_for_location
from fastapi.encoders import jsonable_encoder
import requests

app = FastAPI()

@app.post("/ingest")
def read_external_data():
    data = ingest_weather_for_location("London")
    json_data = jsonable_encoder(data)

    url = "http://0.0.0.0:8001"
    response = requests.post(url, json_data)

    return response

