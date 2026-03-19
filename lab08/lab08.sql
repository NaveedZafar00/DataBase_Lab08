CREATE OR REPLACE FUNCTION get_coordinates_in_range()
RETURNS TABLE (
    airport_code character(3),
    coordinates point
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ad.airport_code,
        ad.coordinates
    FROM airports_data ad
    WHERE 
        CAST(ad.coordinates[0] AS double precision) BETWEEN 35 AND 50
        AND CAST(ad.coordinates[1] AS double precision) BETWEEN 35 AND 50;
END;
$$;




