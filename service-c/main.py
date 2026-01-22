from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
import os
import time

# =====================
# Environment variables
# =====================
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass123")
DB_NAME = os.getenv("DB_NAME", "weather_db")

TABLE_NAME = "records_weather"

app = FastAPI(title="Service C – Data Storage & Light Analytics SQL")

# =====================
# DB helpers
# =====================
def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_db(retries: int = 10, delay: int = 2):
    """
    Initialize database and table with retry logic
    (waits for MySQL to be ready)
    """
    last_error = None

    for attempt in range(retries):
        try:
            # Create DB if not exists
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cur.close()
            conn.close()

            # Create table if not exists
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp VARCHAR(32),
                    location_name VARCHAR(100),
                    country VARCHAR(100),
                    latitude DOUBLE,
                    longitude DOUBLE,
                    temperature DOUBLE,
                    humidity DOUBLE,
                    wind_speed DOUBLE,
                    temperature_category VARCHAR(20),
                    wind_status VARCHAR(20)
                )
            """)
            conn.commit()
            cur.close()
            conn.close()

            print("DB initialized successfully")
            return

        except mysql.connector.Error as e:
            last_error = e
            print(f"DB not ready yet (attempt {attempt + 1}/{retries}), retrying...")
            time.sleep(delay)

    raise RuntimeError(
        f"DB initialization failed after {retries} attempts: {last_error}"
    )


# =====================
# Startup hook
# =====================
@app.on_event("startup")
def startup_event():
    init_db()


# =====================
# Endpoints
# =====================
@app.post("/records")
def store_records(data: list[dict]):
    """
    Receive normalized records from Service B and store them in MySQL
    """
    json_data = jsonable_encoder(data)

    try:
        conn = get_conn()
        cur = conn.cursor()

        sql = f"""
            INSERT INTO {TABLE_NAME}
            (timestamp, location_name, country, latitude, longitude,
             temperature, humidity, wind_speed, temperature_category, wind_status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = [
            (
                r.get("timestamp"),
                r.get("location_name"),
                r.get("country"),
                r.get("latitude"),
                r.get("longitude"),
                r.get("temperature"),
                r.get("humidity"),
                r.get("wind_speed"),
                r.get("temperature_category"),
                r.get("wind_status"),
            )
            for r in json_data
        ]

        cur.executemany(sql, values)
        conn.commit()

        inserted = cur.rowcount
        cur.close()
        conn.close()

        return {"inserted": inserted}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records")
def get_records(limit: int = 200):
    """
    Return sample records
    """
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(f"SELECT * FROM {TABLE_NAME} LIMIT %s", (limit,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"count": len(rows), "data": rows}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records/count")
def count_by_country():
    """
    Count records per country
    """
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(f"""
            SELECT country, COUNT(*) AS count
            FROM {TABLE_NAME}
            GROUP BY country
        """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"data": rows}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records/avg-temperature")
def avg_temperature_by_country():
    """
    Average temperature per country
    """
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(f"""
            SELECT country, AVG(temperature) AS avg_temperature
            FROM {TABLE_NAME}
            GROUP BY country
        """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"data": rows}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records/max-wind")
def max_wind_by_country():
    """
    Max wind speed per country
    """
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(f"""
            SELECT country, MAX(wind_speed) AS max_wind_speed
            FROM {TABLE_NAME}
            GROUP BY country
        """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"data": rows}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records/extreme")
def extreme_records(limit: int = 200):
    """
    Extreme conditions:
    calm + hot OR windy + cold
    """
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(f"""
            SELECT *
            FROM {TABLE_NAME}
            WHERE
                (wind_status = 'calm' AND temperature_category = 'hot')
                OR
                (wind_status = 'windy' AND temperature_category = 'cold')
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {"count": len(rows), "data": rows}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
