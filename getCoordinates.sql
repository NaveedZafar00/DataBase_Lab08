CREATE OR REPLACE FUNCTION getCoordinates()
RETURNS TABLE(coordinates point)
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT a.Coordinates
	FROM AIRPORTS_DATA AS a
	WHERE a.Coordinates[0] >= 35 AND a.Coordinates[0] <= 50 AND
		  a.Coordinates[1] >= 35 AND a.Coordinates[1] <= 50;
END;
$$;

SELECT * FROM Address;