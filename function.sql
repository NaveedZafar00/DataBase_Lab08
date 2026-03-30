CREATE OR REPLACE FUNCTION get_airports()
RETURNS TABLE (coordinates point) AS $$
BEGIN
    RETURN QUERY
    SELECT
        airports_data.coordinates
    FROM airports_data
    WHERE airports_data.coordinates[0] >= 35
      AND airports_data.coordinates[0] <= 50
      AND airports_data.coordinates[1] >= 35
      AND airports_data.coordinates[1] <= 50;
END;
$$ LANGUAGE plpgsql;