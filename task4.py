import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

conn = psycopg2.connect(
    host="localhost",
    database="demo",
    user="postgres",
    password="580115"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings.address (
    address_id SERIAL PRIMARY KEY,
    address_text TEXT,
    address_x DOUBLE PRECISION,
    address_y DOUBLE PRECISION
);
""")
conn.commit()

cur.execute("SELECT * FROM bookings.get_coordinates_in_range();")
rows = cur.fetchall()

geolocator = Nominatim(user_agent="lab08_app")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

for row in rows:
    airport_code, x, y = row

    location = reverse((y, x), exactly_one=True)

    if location:
        address_text = location.address
    else:
        address_text = "Address not found"

    cur.execute("""
        INSERT INTO bookings.address (address_text, address_x, address_y)
        VALUES (%s, %s, %s);
    """, (address_text, x, y))
    conn.commit()

    print(airport_code, address_text)

cur.close()
conn.close()