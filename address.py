import psycopg2
from geopy.geocoders import Nominatim
import time

conn = psycopg2.connect(
    host="localhost",
    port=45432,
    database="demo",
    user="postgres",
    password="postgres"
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
conn.commit()

cur.execute("SELECT * FROM get_filtered_coordinates() LIMIT 10;")
results = cur.fetchall()

geolocator = Nominatim(user_agent="my_app")

for row in results:
    lon = row[2]
    lat = row[3]
    
    try:
        location = geolocator.reverse(f"{lat}, {lon}")
        address = location.address if location else "Address not found"
    except:
        address = "Geocoding failed"
    
    cur.execute("""
        INSERT INTO Address (address_text, address_x, address_y)
        VALUES (%s, %s, %s)
    """, (address, lon, lat))
    conn.commit()
    
    time.sleep(1)

cur.close()
conn.close()
