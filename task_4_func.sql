DROP FUNCTION IF EXISTS get_airports_in_range();

CREATE OR REPLACE FUNCTION get_airports_in_range()
RETURNS TABLE (x FLOAT, y FLOAT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT (coordinates)[0]::FLOAT, (coordinates)[1]::FLOAT
    FROM airports_data
    WHERE (coordinates)[0] BETWEEN 35 AND 50
    AND (coordinates)[1] BETWEEN 35 AND 50;
END;
$$;