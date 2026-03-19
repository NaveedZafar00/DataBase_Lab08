import psycopg2
from geopy.geocoders import Nominatim
import time
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Address (
    address_id SERIAL PRIMARY KEY,
    address_text TEXT,
    address_x FLOAT,
    address_y FLOAT
);
""")

cur.execute("SELECT * FROM get_coordinates();")
rows = cur.fetchall()

geolocator = Nominatim(user_agent="geo_app")

for row in rows:
    coords = row[1]  

    coords = coords.strip("()").split(",")

    lat = float(coords[0])
    lon = float(coords[1])

    try:
        location = geolocator.reverse(f"{lat}, {lon}")

        if location:
            address = location.address

            cur.execute("""
            INSERT INTO Address (address_text, address_x, address_y)
            VALUES (%s, %s, %s)
            """, (address, lat, lon))

            print(f"[{lat}, {lon}] → {address}")

        time.sleep(1) 

    except Exception as e:
        print("Error:", e)

conn.commit()
cur.close()
conn.close()

