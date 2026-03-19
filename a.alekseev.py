import psycopg2
from geopy.geocoders import Nominatim
import time


def retrieve_and_geocode():
    params = {
        'host': 'localhost',
        'database': 'demo',
        'user': 'postgres',
        'password': '565856'
    }
    geolocator = Nominatim(user_agent="my_geocoder")


    with psycopg2.connect(**params) as db:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM retrieve_addresses()")
            rows = cur.fetchall()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Address (
                    address_id SERIAL PRIMARY KEY,
                    address_text TEXT,
                    address_x NUMERIC,
                    address_y NUMERIC
                )
            """)
            for row in rows:
                point = row[0] 
                point_str = point.strip('()')
                lon_str, lat_str = point_str.split(',')
                lon = float(lon_str)
                lat = float(lat_str)
                location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True, language='en')
                address = location.address if location else None

                cur.execute(
                    "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s)",
                    (address, lon, lat)
                )
                time.sleep(1) 
            db.commit()
            print("Success")

if __name__ == '__main__':
    retrieve_and_geocode()