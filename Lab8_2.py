import psycopg2

print("START TASK 2")

conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    dbname="demo",
    user="postgres",
    password="1234"
)
print("CONNECTED")

cur = conn.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION retrieve_flights_page(page_size INT, page_number INT)
RETURNS TABLE (
    flight_id INT,
    flight_no CHAR(6),
    departure_airport CHAR(3),
    arrival_airport CHAR(3)
)
AS $$
BEGIN

    IF page_size < 0 OR page_number < 0 THEN
        RAISE EXCEPTION 'negative values not allowed';
    END IF;

    RETURN QUERY
    SELECT
        f.flight_id,
        f.flight_no,
        f.departure_airport,
        f.arrival_airport
    FROM bookings.flights f
    ORDER BY f.flight_id
    OFFSET (page_number - 1) * page_size
    LIMIT page_size;

END;
$$ LANGUAGE plpgsql;
""")

conn.commit()
print("FUNCTION CREATED")

cur.execute("SELECT * FROM retrieve_flights_page(100, 3);")
rows = cur.fetchall()

print("RESULT:")
for row in rows[:10]:
    print(row)

print("TOTAL ROWS:", len(rows))

cur.close()
conn.close()