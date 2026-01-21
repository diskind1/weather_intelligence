from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np

app = FastAPI(title="Service B - Data Cleaning & Normalization")

@app.post("/clean")
def clean(data: list[dict]):

    
    df = pd.DataFrame(data)

    
    required_cols = ["timestamp", "location_name", "temperature", "wind_speed"]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing field: {col}")

   
    df["temperature_category"] = pd.cut(
        x = df["temperature"],
        bins=[-np.inf, 18, 25, np.inf],
        labels=["cold", "moderate", "hot"]
    )

  
    df["wind_status"] = pd.cut(
    x=df["wind_speed"],
    bins=[-np.inf, 10, np.inf],
    labels=["calm", "windy"]
)

    

    res = {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }

    return res
