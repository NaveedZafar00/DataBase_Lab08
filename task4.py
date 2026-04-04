import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

DB_CONFIG = {
    "dbname": "demo",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT coord_x, coord_y 
        FROM get_filtered_coordinates() 
        LIMIT 5;
    """)
    coords_list = cursor.fetchall()

    print(f"Function returned {len(coords_list)} pairs (limited to 5).")

    if not coords_list:
        print("No coordinates in range.")
        conn.close()
        return

    # geoPy setup
    geolocator = Nominatim(user_agent="task4_airports")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1.1)

    # Create table exactly as required
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Address" (
            address_id    SERIAL PRIMARY KEY,
            address_text  TEXT,
            address_x     DOUBLE PRECISION,
            address_y     DOUBLE PRECISION
        )
    """)

    # Process with geoPy
    for idx, (x, y) in enumerate(coords_list, start=1):
        try:
            location = reverse((x, y))          # change to (y, x) if lat/lon swapped
            address_text = location.address if location else "Address not found"
        except Exception as e:
            address_text = f"Error: {str(e)[:100]}"

        cursor.execute("""
            INSERT INTO "Address" (address_text, address_x, address_y)
            VALUES (%s, %s, %s)
        """, (address_text, x, y))

        print(f"[{idx}/5] ({x:.6f}, {y:.6f}) → {address_text[:80]}...")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()