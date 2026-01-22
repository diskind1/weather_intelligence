# Weather Intelligence – Mini Data Engineering Pipeline

## Overview
This project implements a **3‑microservice data pipeline** for weather data ingestion, processing, and analytics.

**Flow:**
Client → Service A → Service B → Service C → MySQL

## Services
### Service A – Ingestion
- Fetches weather data from an external API (Open‑Meteo)
- Supports multiple locations
- Forwards raw data to Service B

### Service B – Cleaning & Normalization
- Cleans and normalizes incoming data
- Adds derived fields:
  - `temperature_category`
  - `wind_status`
- Forwards processed records to Service C

### Service C – Persistence & Analytics
- Stores records in MySQL
- Exposes analytics endpoints:
  - Count by country
  - Average temperature by country
  - Max wind speed by country
  - Extreme weather records

---

## Project Structure
```
weather_intelligence/
│
├── service-a/
│   ├── main.py
│   ├── api_extractor.py
│   └── Dockerfile
│
├── service-b/
│   ├── main.py
│   └── Dockerfile
│
├── service-c/
│   ├── main.py
│   └── Dockerfile
│
├── docker-compose.yml
│
└── openshift/
    ├── mysql-pvc.yaml
    ├── mysql.yaml
    ├── service-a.yaml
    ├── service-b.yaml
    └── service-c.yaml
```

---

## Run Locally (Docker Compose)

### Build & Run
```bash
docker compose down
docker compose up -d --build
docker compose ps
```

### Trigger the Pipeline
PowerShell:
```powershell
Invoke-RestMethod -Method POST -Uri http://localhost:8001/ingest
```

Expected response:
```json
{
  "inserted": 576
}
```

---

## Service C – API Examples (Local)

```powershell
Invoke-RestMethod -Uri "http://localhost:8003/records?limit=5"
Invoke-RestMethod -Uri "http://localhost:8003/records/count"
Invoke-RestMethod -Uri "http://localhost:8003/records/avg-temperature"
Invoke-RestMethod -Uri "http://localhost:8003/records/max-wind"
Invoke-RestMethod -Uri "http://localhost:8003/records/extreme?limit=5"
```

---

## Run on OpenShift

### Apply Resources (order is important)
```bash
oc apply -f openshift/mysql-pvc.yaml
oc apply -f openshift/mysql.yaml
oc apply -f openshift/service-c.yaml
oc apply -f openshift/service-b.yaml
oc apply -f openshift/service-a.yaml
```

### Trigger via Route
```powershell
$routeHost = (oc get route service-a -o jsonpath='{.spec.host}')
Invoke-RestMethod -Method POST -Uri ("https://" + $routeHost + "/ingest")
```

---

## Notes
- Only **Service A** is exposed externally (Route).
- Services B and C are internal cluster services.
- Database tables are created automatically by Service C on startup.
- Docker Compose `version` field is intentionally omitted (Compose v2+).

---

## Status
✅ Local run successful  
✅ OpenShift deployment successful  
✅ All required endpoints operational  
