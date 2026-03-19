from geopy.geocoders import Nominatim
import psycopg2


con = psycopg2.connect(database="demo", user="postgres",
                        password="postgres", host="127.0.0.1", port="5432")
cur = con.cursor()
cur.callproc('getCoordinates')
rows = cur.fetchall()
cur.execute('CREATE TABLE IF NOT EXISTS Address (' \
            ' address_id INT PRIMARY KEY,' \
            'address_text VARCHAR(200),' \
            'address_x DOUBLE PRECISION,' \
            'address_y DOUBLE PRECISION' \
            ')')

geolocator = Nominatim(user_agent="airport decoder")

for i in range(len(rows)):
    point = rows[i][0][1:-1]
    location = geolocator.reverse(point)
    x, y = map(float, point.split(','))
    address_location = location.address if location else None
    cur.execute('INSERT INTO Address (address_id, address_text, address_x, address_y) VALUES (%s, %s, %s, %s)',
                (i, address_location, x, y))

con.commit()
cur.close()
con.close()

