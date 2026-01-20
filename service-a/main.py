from fastapi import FastAPI
from api_extractor import ingest_weather_for_location
from fastapi.encoders import jsonable_encoder

app = FastAPI()

@app.post("/ingest")
def read_external_data():
    # this triggers the whole pipeline to ingest weather for London and write to mysql
    data = ingest_weather_for_location("London")
    json_data = jsonable_encoder(data)
    return json_data
