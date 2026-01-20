from fastapi import FastAPI, HTTPException
import pandas as pd
import requests
import uvicorn

app = FastAPI(title="Service B - Data Cleaning & Normalization")

url = "http://0.0.0.0:8001/ingest"

# SERVICE_C_URL = ("SERVICE_C_URL", "http://localhost:8003")


@app.post("/clean")
def clean():





    response = requests.get(url)
    # response.raise_for_status()
    data = response.json()

    return data





# df.to_dict(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)