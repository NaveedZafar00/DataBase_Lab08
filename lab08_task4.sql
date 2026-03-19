CREATE OR REPLACE FUNCTION bookings.get_coordinates_in_range()
RETURNS TABLE (
    airport_code CHAR(3),
    coord_x DOUBLE PRECISION,
    coord_y DOUBLE PRECISION
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.airport_code,
        a.coordinates[0],
        a.coordinates[1]
    FROM bookings.airports_data a
    WHERE 
        a.coordinates[0] BETWEEN 35 AND 50
        AND a.coordinates[1] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;