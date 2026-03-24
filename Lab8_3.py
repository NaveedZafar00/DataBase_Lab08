import psycopg2

print("START TASK 3")

conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    dbname="demo",
    user="postgres",
    password="1234"
)

cur = conn.cursor()


cur.execute("""
CREATE OR REPLACE FUNCTION check_flight_time()
RETURNS TRIGGER AS $$
BEGIN

    -- scheduled время
    IF NEW.scheduled_arrival <= NEW.scheduled_departure THEN
        RAISE EXCEPTION 'scheduled arrival must be after departure';
    END IF;

    -- actual время
    IF NEW.actual_departure IS NOT NULL AND NEW.actual_arrival IS NOT NULL THEN
        IF NEW.actual_arrival <= NEW.actual_departure THEN
            RAISE EXCEPTION 'actual arrival must be after actual departure';
        END IF;
    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;
""")

print("FUNCTION CREATED")

# trigger
cur.execute("""
DROP TRIGGER IF EXISTS trigger_check_time ON bookings.flights;

CREATE TRIGGER trigger_check_time
BEFORE INSERT OR UPDATE ON bookings.flights
FOR EACH ROW
EXECUTE FUNCTION check_flight_time();
""")

conn.commit()

print("TRIGGER CREATED")

# TEST 1
print("VALID TEST")
try:
    cur.execute("""
    INSERT INTO bookings.flights (
        flight_id,
        flight_no,
        scheduled_departure,
        scheduled_arrival,
        departure_airport,
        arrival_airport,
        status,
        aircraft_code,
        actual_departure,
        actual_arrival
    )
    VALUES (
        999101,
        'TSK401',
        now(),
        now() + interval '2 hours',
        'DME',
        'LED',
        'Scheduled',
        '320',
        NULL,
        NULL
    );
    """)
    conn.commit()
    print("valid test passed")
except Exception as e:
    conn.rollback()
    print("valid test failed:", e)

# TEST 2
print("INVALID TEST")
try:
    cur.execute("""
    INSERT INTO bookings.flights (
        flight_id,
        flight_no,
        scheduled_departure,
        scheduled_arrival,
        departure_airport,
        arrival_airport,
        status,
        aircraft_code,
        actual_departure,
        actual_arrival
    )
    VALUES (
        999102,
        'TSK402',
        now(),
        now() - interval '2 hours',
        'DME',
        'LED',
        'Scheduled',
        '320',
        NULL,
        NULL
    );
    """)
    conn.commit()
    print("invalid test passed (wrong)")
except Exception as e:
    conn.rollback()
    print("invalid test blocked:", e)

cur.close()
conn.close()

print("END TASK 3")