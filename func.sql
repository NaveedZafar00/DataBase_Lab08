DROP FUNCTION IF EXISTS get_coordinates();

CREATE FUNCTION get_coordinates()
RETURNS TABLE (
    airport_code CHAR(3),
    coordinates TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.airport_code,
        a.coordinates::TEXT
    FROM airports_data a
    WHERE 
        (a.coordinates[0] BETWEEN 35 AND 50)
        AND
        (a.coordinates[1] BETWEEN 35 AND 50)
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

--SELECT * FROM get_coordinates();