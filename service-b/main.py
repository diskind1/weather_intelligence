from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import requests

app = FastAPI(title="Service B - Data Cleaning & Normalization")

SERVICE_C_URL = "http://127.0.0.1:8003/records"

@app.post("/clean")
def clean(data: list[dict]):
    df = pd.DataFrame(data)

    required_cols = [
        "timestamp", "location_name", "country",
        "latitude", "longitude",
        "temperature", "wind_speed", "humidity"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing field: {col}")

    df["temperature_category"] = pd.cut(
        df["temperature"], bins=[-np.inf, 18, 25, np.inf],
        labels=["cold", "moderate", "hot"]
    ).astype(str)

    df["wind_status"] = pd.cut(
        df["wind_speed"], bins=[-np.inf, 10, np.inf],
        labels=["calm", "windy"]
    ).astype(str)

    cleaned = df.to_dict(orient="records")

    try:
        r = requests.post(SERVICE_C_URL, json=cleaned, timeout=60)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=r.text)
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
