CREATE OR REPLACE FUNCTION get_airports_coordinates()
RETURNS TABLE(airport_code CHAR(3), latitude double precision, longitude double precision) AS $$
BEGIN
    RETURN QUERY
    SELECT a.airport_code,
           a.coordinates[1] as latitude,
           a.coordinates[0] as longitude
    FROM airports_data a
    WHERE a.coordinates[1] BETWEEN 35 AND 50
      AND a.coordinates[0] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;