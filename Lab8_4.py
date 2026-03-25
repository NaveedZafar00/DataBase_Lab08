import psycopg2
from geopy.geocoders import Nominatim
import time

print("START TASK 4")

conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    dbname="demo",
    user="postgres",
    password="1234"
)

cur = conn.cursor()

# function
cur.execute("""
CREATE OR REPLACE FUNCTION get_airports_in_range()
RETURNS TABLE (
    airport_code CHAR(3),
    address_x FLOAT,
    address_y FLOAT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.airport_code,
        a.coordinates[0]::FLOAT,
        a.coordinates[1]::FLOAT
    FROM bookings.airports_data a
    WHERE a.coordinates[0] BETWEEN 35 AND 50
      AND a.coordinates[1] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;
""")

conn.commit()
print("FUNCTION CREATED")

# table
cur.execute("""
DROP TABLE IF EXISTS Address;

CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    address_text TEXT,
    address_x FLOAT,
    address_y FLOAT
);
""")

conn.commit()
print("TABLE CREATED")

# get coordinates
cur.execute("SELECT * FROM get_airports_in_range();")
rows = cur.fetchall()

print("ROWS FOUND:", len(rows))

geolocator = Nominatim(user_agent="lab8_task4")

saved_count = 0

for row in rows:
    airport_code = row[0]
    x = row[1]
    y = row[2]

    try:
        location = geolocator.reverse(f"{y}, {x}")
        if location is not None:
            address_text = location.address
        else:
            address_text = "address not found"

        cur.execute("""
        INSERT INTO Address (address_text, address_x, address_y)
        VALUES (%s, %s, %s);
        """, (address_text, x, y))

        conn.commit()

        print("saved for", airport_code)
        saved_count += 1

        time.sleep(1)

    except Exception as e:
        print("error for", airport_code, ":", e)

print("TOTAL SAVED:", saved_count)

cur.execute("SELECT * FROM Address;")
result = cur.fetchall()

print("ADDRESS TABLE:")
for item in result:
    print(item)

cur.close()
conn.close()

print("END TASK 4")