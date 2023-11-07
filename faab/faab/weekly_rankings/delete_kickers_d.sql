delete from api_target where api_target.id in (select at2.id  from api_target at2 join api_player ap on at2.player_id = ap.id where ap.position_id > 4 and at2.week = 23)
