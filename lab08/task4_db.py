import psycopg2
from geopy.geocoders import Nominatim
import time
import re

conn = psycopg2.connect(
    database="demo",
    user="postgres",
    password="12345",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()
print("Connected to database")


cur.execute('''
    CREATE TABLE IF NOT EXISTS Address (
        address_id SERIAL PRIMARY KEY,
        address_text TEXT,
        address_x DOUBLE PRECISION,
        address_y DOUBLE PRECISION
    )
''')
conn.commit()


cur.execute("SELECT * FROM get_coordinates_in_range();")
results = cur.fetchall()
print(f"Found {len(results)} airports in range")


def parse_point(point_str):
    match = re.search(r'\(([^,]+),([^)]+)\)', point_str)
    return float(match.group(1)), float(match.group(2))


geolocator = Nominatim(user_agent="my_app")


for row in results:
    airport_code = row[0].strip()
    point_str = row[1]

    lon, lat = parse_point(point_str)
    print(f"\nProcessing {airport_code}: ({lat}, {lon})")

    location = geolocator.reverse(f"{lat}, {lon}")
    address = location.address if location else "Address not found"
    print(f"Address: {address[:50]}...")

    cur.execute('''
        INSERT INTO Address (address_text, address_x, address_y)
        VALUES (%s, %s, %s)
    ''', (address, lon, lat))
    conn.commit()

    time.sleep(1)


cur.execute("SELECT * FROM Address;")
for row in cur.fetchall():
    print(row)


cur.close()
conn.close()
