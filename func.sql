CREATE OR REPLACE FUNCTION get_filtered_coordinates()
RETURNS TABLE (
    airport_code character(3),
    airport_name jsonb,
    longitude double precision,
    latitude double precision
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.airport_code,
        a.airport_name,
        a.coordinates[0] AS longitude,
        a.coordinates[1] AS latitude
    FROM airports_data a
    WHERE 
        a.coordinates[1] BETWEEN 35 AND 50
        AND a.coordinates[0] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;
