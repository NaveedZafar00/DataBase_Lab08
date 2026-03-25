DROP FUNCTION IF EXISTS retrieve_Flights(INT, INT);

CREATE OR REPLACE FUNCTION retrieve_Flights(start_idx INT, end_idx INT)
RETURNS TABLE(
	flight_id INT, 
	flight_no CHAR(6), 
	scheduled_departure timestamp with time zone, 
	scheduled_arrival timestamp with time zone
)
LANGUAGE plpgsql
AS $$
BEGIN
	IF start_idx < 0 OR end_idx < 0 THEN
		RAISE EXCEPTION 'start and end should not be negative';
	END IF;
	RETURN QUERY 
	SELECT f.flight_id, f.flight_no, f.scheduled_departure, f.scheduled_arrival
	FROM flights f
	ORDER BY f.flight_id ASC
	OFFSET start_idx - 1
	LIMIT (end_idx - start_idx + 1);
END;
$$;

SELECT * FROM retrieve_Flights(20, 60);

