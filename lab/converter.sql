CREATE FUNCTION converter()
RETURNS TABLE (
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        coordinates[0]::DOUBLE PRECISION,
        coordinates[1]::DOUBLE PRECISION
    FROM airports_data
    WHERE coordinates[0] BETWEEN 35 AND 50
      AND coordinates[1] BETWEEN 35 AND 50;
END;
$$
LANGUAGE plpgsql;
