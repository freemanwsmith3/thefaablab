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
try:


    con = psycopg2.connect(
        host='ec2-34-199-68-114.compute-1.amazonaws.com',
        user='oibdolfaruxway',
        password='5983be3a6ab94c50df024487d2c3bcbab6a2eca9a8b4c594ddaf0b934a5553cc',
        database='d4qgddmcqs7su1'
    )
    cur = con.cursor()

    


    df = pd.read_csv('./faab/faab/stats/2024rankings.csv')

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
            if position == "DS":
                pos_id= 5
            if position[0] == "K":
                pos_id = 6       

            print('new team id', team_id)
            print('---------')
        # cur.execute("""insert into api (week, player_id) values (%s, %s);""", [week, player_id] )
        except Exception as e:
            print(e)
        
        # link  = 'https://www.nfl.com/players/' + slugify(name) + '/'
        # print(row['PLAYER NAME'])
        # print(team)
        # print('-----------------------')
        # if row['PLAYER NAME'] not in players_set:
        #     print("===========================")
        
    
        #     print("name:", name )
        #     print("TEAM: ", team_id)
        #     print("position_id: ", pos_id)
        #     print("LINK: ", link)
        #     try:
        #         cur.execute("""insert into api_player (name, team_id, position_id, link, image) values (%s, %s, %s, %s, %s);""", [name, team_id, pos_id, link, name] )
        #         con.commit()
        #     except Exception as e:
        #         print(e)
        #     else:
        #         print("DEFENSE", name)
            
    # # cur.execute("""SELECT * FROM api_player""")
    # # players = cur.fetchall()
    # # player_id_dict = {}
    # # for player in players:
    # #     player_id_dict[player[1]] = player[0]

    # # ranking_to_insert = []
    # # for index,row in  df.iterrows():
    # #     insert_tuple = (row["RK"], player_id_dict[row["PLAYER NAME"]], 'fantasy_pros', 0, "now")
    # #     ranking_to_insert.append(insert_tuple)
    # # insert_query = """INSERT INTO api_ranking ("rank", "Player_id", "user", "week", "created_at") VALUES (%s, %s, %s, %s, %s)"""
    # # cur.executemany(insert_query, ranking_to_insert)
    # con.commit()
    con.close()
    
except Exception as e:
    print("Couldn't conect ", e)
