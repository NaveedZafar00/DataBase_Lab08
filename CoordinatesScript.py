import psycopg2
from geopy.geocoders import Nominatim
import time

with open('function_creation.sql', 'r', encoding='utf-8') as file:
    sql_function = file.read()

# data to connect to the database (locally)
conn = psycopg2.connect(
    host="localhost",
    database="demo",
    user="postgres",
    password=""
)
cursor = conn.cursor()

# creating the function for retrieving coordinates from the database
cursor.execute(sql_function)
conn.commit()

# creating the table for addresses
cursor.execute("""
    DROP TABLE IF EXISTS Address;
    CREATE TABLE Address (
        address_id SERIAL PRIMARY KEY,
        address_text TEXT,
        address_x DECIMAL(10, 7),
        address_y DECIMAL(10, 7)
    );
""")
conn.commit()

# using the function created earlier
cursor.execute("SELECT * FROM get_airports_coordinates();")
airports = cursor.fetchall()

# crerating the geolocator using geopy
geolocator = Nominatim(user_agent="lab8_task4")

for airport_code, lat, lon in airports:

    # catching errors if any
    try:
        # getting addresses by coordinates using geopy
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
        address = location.address if location else "Address not found"
    except:
        address = "Geocoding failed"

    # inserting the found addresses into the new table
    cursor.execute(
        "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s);",
        (address, lon, lat)
    )
    conn.commit()
    # necessary for a correct work of Nominatim
    time.sleep(1)

cursor.close()
conn.close()
