create or replace function get_valid_coordinates(limit_cnt int)
returns table(x float, y float)
as $$
begin
    return QUERY
    select coordinates[1], coordinates[2]
      from airports_data
     where coordinates[1] between 35 and 50
       and coordinates[2] between 35 and 50
     limit limit_cnt;
end;
$$ language plpgsql;