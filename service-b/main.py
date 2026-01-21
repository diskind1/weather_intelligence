from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Service B - Data Cleaning & Normalization")

@app.post("/clean")

def clean(data):

    clean_data = [data]
    # for loc in data:
    #     clean_data.append(loc.get("location_name"))

    return clean_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
