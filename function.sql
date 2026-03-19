CREATE OR REPLACE FUNCTION get_airports_in_range()
RETURNS TABLE (
    airport_code CHAR(3),
    address_x DOUBLE PRECISION,
    address_y DOUBLE PRECISION
)
LANGUAGE plpgsql
AS $$
    SELECT
        a.airport_code,
        a.coordinates[0] AS address_x,
        a.coordinates[1] AS address_y
    FROM airports_data a
    WHERE a.coordinates[0] BETWEEN 35 AND 50
      AND a.coordinates[1] BETWEEN 35 AND 50
    ORDER BY a.airport_code;
$$;