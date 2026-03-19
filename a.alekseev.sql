CREATE OR REPLACE FUNCTION retrieve_addresses()
RETURNS TABLE (
	coordinates point 
)
AS $$
BEGIN
 RETURN QUERY
 SELECT a.coordinates 
 FROM airports_data a
 WHERE (a.coordinates)[0] BETWEEN 35 AND 50
 AND (a.coordinates)[1] BETWEEN 35 AND 50;
END;
$$ LANGUAGE plpgsql;