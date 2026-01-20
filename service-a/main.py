from fastapi import FastAPI
from api_extractor import ingest_weather_for_location

app = FastAPI()

@app.post("/ingest")
def read_external_data():
    # this triggers the whole pipeline to ingest weather for London and write to mysql
    data = ingest_weather_for_location("London")
    return data

