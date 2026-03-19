import psycopg2
from geopy.geocoders import Nominatim
import time

conn = psycopg2.connect(
    database="db_lab8",
    user="postgres",
    password="111111",
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()
print("Connected to database")

cur.execute("""
CREATE TABLE IF NOT EXISTS Address (
    address_id SERIAL PRIMARY KEY,
    address_text TEXT,
    address_x FLOAT,
    address_y FLOAT
);
""")
conn.commit()

cur.execute("SELECT * FROM get_valid_coordinates(10);")
rows = cur.fetchall()

print(f"Fetched {len(rows)} coordinates")

geolocator = Nominatim(user_agent="geo_app")

for row in rows: # Process coordinates
    x, y = row
    try:
        location = geolocator.reverse(f"{x}, {y}", timeout=10)
        
        if location:
            address = location.address
            print(f"{x}, {y} -> {address}")

            cur.execute("""
                INSERT INTO Address (address_text, address_x, address_y)
                VALUES (%s, %s, %s)
            """, (address, x, y))
            conn.commit()

        else:
            print(f"{x}, {y} -> No address found")

        time.sleep(1)

    except Exception as e:
        print(f"Error with {x}, {y}: {e}")

cur.close()
conn.close()
print("Done")