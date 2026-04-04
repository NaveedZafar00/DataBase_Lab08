CREATE OR REPLACE FUNCTION get_filtered_coordinates()
RETURNS TABLE (coord_x DOUBLE PRECISION, coord_y DOUBLE PRECISION)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        coordinates[0] AS coord_x,
        coordinates[1] AS coord_y
    FROM airports_data
    WHERE coordinates IS NOT NULL
      AND coordinates[0] BETWEEN 35 AND 50
      AND coordinates[1] BETWEEN 35 AND 50;
END;
$$;