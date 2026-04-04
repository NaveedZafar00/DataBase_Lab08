import psycopg2
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

#Connection setingss
DB_CONFIG = {
    "dbname": "demo", 
    "user": "postgres",
    "password": "PIGEon3308!",
    "host": "localhost",
    "port": "5432",
    "client_encoding": "utf8"
}

#Converts coordinates into an address
geolocator = Nominatim(user_agent="airports_to_address")
reverse_geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def main():
    conn = None
    try:
        #Connect to databse
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        cur = conn.cursor()
        print("Connection to data base created.")

        #Call the function
        cur.execute("SELECT * FROM get_airports_in_range();")
        rows = cur.fetchall()
        print(f"Airports found: {len(rows)}")

        if not rows:
            print("There are no airports in the 35-50 range. We are finishing our work.")
            return

        # Create table Address
        cur.execute("""
            DROP TABLE IF EXISTS Address;
            CREATE TABLE Address (
                address_id SERIAL PRIMARY KEY,
                address_text TEXT,
                address_x DOUBLE PRECISION,
                address_y DOUBLE PRECISION
            );
        """)
        conn.commit()
        print("Table Address created.")

        #For each pair of coordinates we obtain the address and insert it into the table
        for row in rows:
            # Taking first two columns as lon and lat
            lon, lat = row[0], row[1]
            try:
                #Address request
                location = reverse_geocode((lat, lon), language='en')
                address = location.address if location else None
                print(f"Coordinates ({lon}, {lat}) -> {address}")
            except Exception as e:
                print(f"Error getting address for ({lon}, {lat}): {e}")
                address = None

            #Insert a row into the table
            cur.execute(
                "INSERT INTO Address (address_text, address_x, address_y) VALUES (%s, %s, %s)",
                (address, lon, lat)
            )
            conn.commit()

        print("Done.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection with DataBase closed.")

if __name__ == "__main__":
    main()