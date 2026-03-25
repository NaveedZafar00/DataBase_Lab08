import psycopg2

print("START TASK 1")

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
CREATE OR REPLACE FUNCTION retrieve_flights(start_idx INT, end_idx INT)
RETURNS TABLE (
    flight_id INT,
    flight_no CHAR(6),
    scheduled_departure TIMESTAMPTZ,
    scheduled_arrival TIMESTAMPTZ
)
AS $$
BEGIN

    IF start_idx < 0 OR end_idx < 0 THEN
        RAISE EXCEPTION 'negative values not allowed';
    END IF;

    RETURN QUERY
    SELECT
        f.flight_id,
        f.flight_no,
        f.scheduled_departure,
        f.scheduled_arrival
    FROM bookings.flights f
    ORDER BY f.flight_id
    OFFSET start_idx - 1
    LIMIT end_idx - start_idx + 1;

END;
$$ LANGUAGE plpgsql;
""")

conn.commit()
print("FUNCTION CREATED")

cur.execute("SELECT * FROM retrieve_flights(10, 60);")
rows = cur.fetchall()

print("RESULT:")
for row in rows:
    print(row)

print("TOTAL ROWS:", len(rows))

cur.close()
conn.close()