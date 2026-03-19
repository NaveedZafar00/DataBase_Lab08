import psycopg2
from geopy.geocoders import Nominatim
import time

# Just to make a connection with DB
conn = psycopg2.connect(
    host="localhost",
    database="demo",
    user="postgres",
    password="FwtOlwnQ73"
)
cur = conn.cursor()

# Paste a sql-code to be executed
cur.execute("SELECT x, y FROM get_filtered_coordinates();")
rows = cur.fetchall()

# Do not know what it is, but AI corrected me with thas string
geolocator = Nominatim(user_agent="my_uniq_app")

# Some more code, where I CREATE a new Table with name "Address"
cur.execute("""
    CREATE TABLE IF NOT EXISTS Address (
        address_id SERIAL PRIMARY KEY,
        address_text TEXT,
        address_x FLOAT,
        address_y FLOAT
    );
""")
conn.commit()

# Thanks to peolpe from the Internet I found this
for x, y in rows:
    # Some help from AI to go through the coordinates
    try:
        location = geolocator.reverse(f"{y}, {x}")
        address = location.address if location else None
    except Exception as e:
        print(f"Error for coordinates ({x}, {y}): {e}")
        address = None

    cur.execute(
        "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s);",
        (address, x, y)
    )
    conn.commit()

    time.sleep(1) # AI said that it should be there

cur.close()
conn.close()