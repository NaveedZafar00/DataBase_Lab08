import psycopg2
from geopy.geocoders import Nominatim
import time

DB_CONFIG = {
    'host': 'localhost',
    'database': 'demo',
    'user': 'postgres',
    'password': '9295342v',
    'client_encoding': 'utf8'
}

def get_filtered_coordinates():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.callproc('filter_coordinates')
    rows = cur.fetchall()
    coords = [(lon, lat) for lon, lat in rows]
    cur.close()
    conn.close()
    return coords

def create_address_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Address (
            address_id SERIAL PRIMARY KEY,
            address_text TEXT,
            address_x NUMERIC,
            address_y NUMERIC
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_address(lon, lat, address_text):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s);",
        (address_text, lon, lat)
    )
    conn.commit()
    cur.close()
    conn.close()

def main():
    create_address_table()
    coordinates = get_filtered_coordinates()
    geolocator = Nominatim(user_agent="airport_address_converter")
    for lon, lat in coordinates:
        location = geolocator.reverse(f"{lat}, {lon}")
        address = location.address if location else None
        insert_address(lon, lat, address)
        time.sleep(1)

if __name__ == "__main__":
    main()