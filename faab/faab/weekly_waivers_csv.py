# Importing the required libraries
from xml.etree.ElementTree import QName
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
from slugify import slugify


# change week below
week = 35
#############


# waiver_pics =  data[data.find('ecrData'):data.find('sosData') ]

# waiver_pics = waiver_pics[waiver_pics.find('{"player_id"'):]
# count = waiver_pics.count('player_owned_yahoo')
try:
    conn = psycopg2.connect(
        host='ec2-52-71-90-133.compute-1.amazonaws.com',
        user='yscnkbjrdccjdm',
        password='abc2e73db2c853ef565d543fe31c401b2f0be626920e7707b705302f6bf519be',
        database='deranomlqt3v7k'
    )
    curr = conn.cursor()


    df = pd.read_csv(f'./faab/faab/stats/waiver_{week-27}.csv')

    # Create a new column 'in_set' which is True if the player's name is in 'my_set' and False otherwise
    for index,row in  df.iterrows():
        name = row['PLAYER NAME']
        print(name)
        position = row['POS'][0:2]
        player_id = None
        team_id = None
        pos_id = None
        team = row['TEAM']
        try:         
            curr.execute("""select id from api_player ap where name = %s;""", [name] )
            player_id = curr.fetchone()[0]
            print(player_id)
            #curr.execute("""select id from api_target ap where player_id = %s;""",[player_id,] )
            # if(curr.fetchone()[0]):
            #     #this skips if already in there
            #     print(curr.fetchone())
            try:
                curr.execute("""insert into api_target (week, player_id) values (%s, %s);""", [week, player_id,] )
                print('executed')
                print('------------------------')
            except Exception as e:
                print(e)
        except Exception as e:
            if position != 'DST' and position[0] != 'K':
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
                if position[0] == "K":
                    pos_id = 6       

                
                link  = 'https://www.nfl.com/players/' + slugify(name) + '/'
                try:
                    print('new player')
                    print(f'Name: {name} | link: {link}')
                    curr.execute("""insert into api_player (name, team_id, position_id, link, image) values (%s, %s, %s, %s, %s);""", [name, team_id, pos_id, link, name] )
                except Exception as e:
                    print(e)
            else:
                print("DEFENSE", name)

    conn.commit()
    conn.close()
    
except Exception as e:
    print("Couldn't conect ", e)
