DROP FUNCTION IF EXISTS retrieveFlightsPage(INT, INT);

CREATE OR REPLACE FUNCTION retrieveFlightsPage(pageSize INT, pageNumber INT)
RETURNS TABLE (
    flight_id INT,
    flight_no CHAR(6),
    departure_airport CHAR(3),
    arrival_airport CHAR(3)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF pageSize < 0 OR pageNumber < 0 THEN
        RAISE EXCEPTION 'pageSize and pageNumber should not be negative';
    END IF;
	RETURN QUERY
    SELECT f.flight_id, f.flight_no, f.departure_airport, f.arrival_airport
    FROM flights f
    ORDER BY f.flight_id ASC
    OFFSET (pageNumber - 1) * pageSize
	LIMIT pageSize;
END;
$$;

SELECT * FROM retrieveFlightsPage(100, 3);