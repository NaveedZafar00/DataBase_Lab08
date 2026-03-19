CREATE FUNCTION filter_coordinates()
RETURNS TABLE(longitude NUMERIC, latitude NUMERIC) 
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (coordinates)[0]::NUMERIC AS lon,
        (coordinates)[1]::NUMERIC AS lat
    FROM airports_data
    WHERE (coordinates)[0] BETWEEN 35 AND 50 AND (coordinates)[1] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;