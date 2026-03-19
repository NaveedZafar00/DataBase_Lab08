import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


DB_NAME = "flights"      # замени на имя своей базы
DB_USER = "postgres"
DB_PASSWORD = "1204"
DB_HOST = "localhost"
DB_PORT = "5432"


def main():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS address (
            address_id SERIAL PRIMARY KEY,
            address_text TEXT,
            address_x DOUBLE PRECISION NOT NULL,
            address_y DOUBLE PRECISION NOT NULL,
            UNIQUE(address_x, address_y)
        );
    """)

    cur.execute("SELECT airport_code, address_x, address_y FROM get_airports_in_range();")
    rows = cur.fetchall()

    geolocator = Nominatim(user_agent="airports_reverse_geocoder")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    for airport_code, x, y in rows:
        try:
            location = reverse((y, x), language="en", exactly_one=True)

            if location is not None:
                address_text = location.address
            else:
                address_text = f"Address not found for airport {airport_code}"

            cur.execute("""
                INSERT INTO address (address_text, address_x, address_y)
                VALUES (%s, %s, %s)
                ON CONFLICT (address_x, address_y) DO NOTHING;
            """, (address_text, x, y))

            print(f"Saved: {airport_code} -> {address_text}")

        except Exception as e:
            print(f"Error for airport {airport_code} ({x}, {y}): {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()