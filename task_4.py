import psycopg2
import time
from geopy.geocoders import Nominatim

DB_CONFIG = {
    "host": "localhost",
    "database": "demo",
    "user": "postgres",
    "password": "Letmein1975!",
    "port": "5432"
}

def get_address(lat, lon, geolocator):
    try:
        location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True, language='en')
        return location.address if location else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("Connected to the database successfully")

    cur.execute("SELECT * FROM get_airports_in_range();")
    rows = cur.fetchall()
    print(f"Found airports: {len(rows)}")

    if not rows:
        cur.close()
        conn.close()
        return

    cur.execute("DROP TABLE IF EXISTS Address;")
    cur.execute("""
        CREATE TABLE Address (
            address_id SERIAL PRIMARY KEY,
            address_text TEXT,
            address_x FLOAT,
            address_y FLOAT
        );
    """)
    conn.commit()

    success = 0
    geolocator = Nominatim(user_agent="airports_geocoder")
    for _, (lon, lat) in enumerate(rows, 1):
        address = get_address(lat, lon, geolocator)
        cur.execute(
            "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s);",
            (address, lon, lat)
        )
        conn.commit()
        success += 1
        time.sleep(1)

    print(f"Done. Processed {success}.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()