import psycopg2
from configparser import ConfigParser
from geopy.geocoders import Nominatim


def load_db_config():
    parser = ConfigParser()
    parser.read('db.ini')
    return dict(parser['postgresql'])


def get_address(x, y):
    geolocator = Nominatim(user_agent="airport_lookup")
    location = geolocator.reverse((x, y))
    return location.address if location else None


def get_airports():
        conn = psycopg2.connect(**load_db_config())
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_airports()")
        coords = []
        for row in cur.fetchall():
            point_str = row[0]
            result = point_str[1:-1].split(',')
            coords.append(tuple(float(c.strip()) for c in result))


        cur.execute("""
            CREATE TABLE IF NOT EXISTS Address (
                address_id SERIAL PRIMARY KEY,
                address_text TEXT,
                address_x DOUBLE PRECISION,
                address_y DOUBLE PRECISION
            )
        """)

        for x, y in coords:
            address_text = get_address(x, y)
            cur.execute("""
                INSERT INTO Address (address_text, address_x, address_y)
                VALUES (%s, %s, %s)
            """, (address_text, x, y))

        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    get_airports()
