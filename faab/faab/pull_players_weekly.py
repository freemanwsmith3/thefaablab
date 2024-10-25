# Importing the required libraries
from xml.etree.ElementTree import QName
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
from slugify import slugify
# Downloading contents of the web page
url = "https://www.fantasypros.com/nfl/rankings/waiver-wire-overall.php"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')
print(soup)

####################
# change week below
week = 28
#############
print('Classes of each table:')

waiver_pics =  data[data.find('ecrData'):data.find('sosData') ]

waiver_pics = waiver_pics[waiver_pics.find('{"player_id"'):]
count = waiver_pics.count('player_owned_yahoo')
try:

    conn = psycopg2.connect(
        host='ec2-52-71-90-133.compute-1.amazonaws.com',
        user='yscnkbjrdccjdm',
        password='abc2e73db2c853ef565d543fe31c401b2f0be626920e7707b705302f6bf519be',
        database='deranomlqt3v7k'
    )
    curr = conn.cursor()


except Exception as e:
    print("Couldn't connect ", e)

print(count)
for i in range(count-1):
    
    res = json.loads(waiver_pics[0:waiver_pics.find(',{"player_id')])
    name = res.get('player_name')
    position = res.get('player_position_id')
    team = res.get('player_team_id')
    print(res)
    player_id = None
    team_id = None
    try:         
        curr.execute("""select id from api_player ap where name = %s;""",[res.get('player_name'),] )
        player_id = curr.fetchone()[0]
        curr.execute("""select id from api_target ap where player_id = %s;""",[player_id,] )
        # if(curr.fetchone()[0]):
        #     #this skips if already in there
        #     print(curr.fetchone())
        curr.execute("""insert into api_target (week, player_id) values (%s, %s);""", [week, player_id,] )
    except Exception as e:
        if position != 'DST' and position != 'K':
            print(name)
            print(position)
            print(team)
            if team == "ARI":
                team_id = 1
            if team == "CHI":
                team_id = 2
            if team == "GB":
                team_id = 3
            if team == "NYG":
                team_id = 4
            if team == "DET":
                team_id = 5
            if team == "WAS":
                team_id = 6
            if team == "PHI":
                team_id = 7
            if team == "PIT":
                team_id = 8
            if team == "LAR":
                team_id = 9
            if team == "SF":
                team_id = 10
            if team == "CLE":
                team_id = 11
            if team == "IND":
                team_id = 12
            if team == "DAL":
                team_id = 13
            if team == "KC":
                team_id = 14
            if team == "LAC":
                team_id = 15
            if team == "DEN":
                team_id = 16
            if team == "NYJ":
                team_id = 17
            if team == "NE":
                team_id = 18
            if team == "LV":
                team_id = 19
            if team == "TEN":
                team_id = 20
            if team == "BUF":
                team_id = 21
            if team == "MIN":
                team_id = 22
            if team == "ATL":
                team_id = 23
            if team == "MIA":
                team_id = 24
            if team == "NO":
                team_id = 25
            if team == "CIN":
                team_id = 26
            if team == "SEA":
                team_id = 27
            if team == "TB":
                team_id = 28
            if team == "CAR":
                team_id = 29
            if team == "JAC":
                team_id = 30
            if team == "BAL":
                team_id = 31
            if team == "TEX" or team == "HOU":
                team_id = 32
            if team == "FA":
                team_id = 33
            ######################
            if position == "RB":
                pos_id = 1
            if position == "WR":
                pos_id = 2
            if position == "QB":
                pos_id = 3
            if position == "TE":
                pos_id = 4
            if position == "K":
                pos_id = 6       

            
            link  = 'https://www.nfl.com/players/' + slugify(name) + '/'
            try:
                print('new player')
                #curr.execute("""insert into api_player (name, team_id, position_id, link, image) values (%s, %s, %s, %s, %s);""", [name, team_id, pos_id, link, name] )
            except Exception as e:
                print(e)
        else:
            print("DEFENSE", name)
        # curr.execute("""insert into api (week, player_id) values (%s, %s);""", [week, player_id] )



    #curr.execute("""insert into api_target (week, player_id) values (%s, %s);""", [week, player_id,] )
    #conn.commit()

    waiver_pics = waiver_pics[1+waiver_pics.find(',{"player_id'):]

    #print(waiver_pics)
conn.close()