CREATE OR REPLACE FUNCTION get_filtered_coordinates()
RETURNS TABLE (x FLOAT, y FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        coordinates[0] AS x,
        coordinates[1] AS y
    FROM airports_data
    WHERE coordinates[0] BETWEEN 35 AND 50
      AND coordinates[1] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;