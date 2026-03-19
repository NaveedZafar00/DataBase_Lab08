import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import getpass

conn = psycopg2.connect(
    dbname="demo",
    user="postgres",
    password=getpass.getpass("password PostgreSQL: "), #write your password, bc I don't want to share mine
    #OR
    #password="yourpassword" if getpass died
    host="localhost",
    port=5432
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Address (
        address_id SERIAL PRIMARY KEY,
        address_text TEXT,
        address_x DOUBLE PRECISION,
        address_y DOUBLE PRECISION
    );
""")

conn.commit()

cur.execute("SELECT lat, lon FROM converter();")
rows = cur.fetchall()

geolocator = Nominatim(user_agent="lab8")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1.3)

added = 0
for row in rows:
    lat = row[0]
    lon = row[1]

    print(f"debug comment: coordinates processing: {lat}, {lon}")

    try:
        loc = reverse((lat, lon))
        if loc:
            cur.execute(
                "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s)",
                (loc.address, lon, lat)
            )
            added += 1
            print(f"debug comment: added: {loc.address[:50]}...")
    except Exception as e:
        print(f"error: {e}")

    time.sleep(1.1)

conn.commit()
cur.close()
conn.close()

print(f"\n yippee!! it works!! added {added} addresses")
