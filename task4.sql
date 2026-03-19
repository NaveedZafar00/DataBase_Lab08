CREATE OR REPLACE FUNCTION get_airports_in_range()
RETURNS TABLE (longitude double precision, latitude double precision) AS $$
BEGIN
    RETURN QUERY
    SELECT (coordinates).x, (coordinates).y
    FROM airports_data
    WHERE (coordinates).x BETWEEN 35 AND 50
      AND (coordinates).y BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;
