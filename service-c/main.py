from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Service C – Data Storage & Light Analytics SQL")

@app.post("/records")
def store(data = Body(...)):
    json_data = jsonable_encoder(data)

    return {"count": len(json_data), "data": json_data}

@app.get("/records")
def store(data):
    return data

@app.post("/records/count")
def store(data):
    return data

@app.post("/records/avg-temperature")
def store(data):
    return data

@app.post("/records/max-wind")
def store(data):
    return data

@app.post("/records/extreme")
def store(data):
    return data
