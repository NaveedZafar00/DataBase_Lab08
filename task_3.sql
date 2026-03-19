CREATE OR REPLACE FUNCTION trigger_flight_times_function()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.scheduled_arrival <= NEW.scheduled_departure THEN
        RAISE EXCEPTION 'Scheduled arrival must be later than scheduled departure';
    END IF;
    IF NEW.actual_departure IS NOT NULL AND NEW.actual_arrival IS NOT NULL THEN
        IF NEW.actual_arrival <= NEW.actual_departure THEN
            RAISE EXCEPTION 'Actual arrival must be later than actual departure';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trigger_flight_times ON flights;

CREATE TRIGGER trigger_flight_times
BEFORE INSERT OR UPDATE ON flights
FOR EACH ROW
EXECUTE FUNCTION trigger_flight_times_function();

UPDATE flights SET scheduled_departure = '2026-05-10 15:00', scheduled_arrival = '2026-05-10 14:00' WHERE flight_id = 1;