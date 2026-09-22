# Importing the required libraries
from xml.etree.ElementTree import QName
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
from slugify import slugify
from db import connect


# waiver_pics =  data[data.find('ecrData'):data.find('sosData') ]

# waiver_pics = waiver_pics[waiver_pics.find('{"player_id"'):]
# count = waiver_pics.count('player_owned_yahoo')
try:

    try: 
        conn = connect()
        curr = conn.cursor()

    except Exception as e:
        print("Can't connect to DB: ", e)

    try: 
        df = pd.read_csv('./faab/faab/stats/2025rankings.csv')

        # Create a new column 'in_set' which is True if the player's name is in 'my_set' and False otherwise
        for index,row in  df.iterrows():
            name = row['PLAYER NAME']
            rank = index 
    except Exception as e: 
        print("can't read csv: ", e)
    
    try:
        curr.execute("""SELECT * FROM api_player""")
        players = curr.fetchall()
        player_id_dict = {}
        for player in players:
            player_id_dict[player[1]] = player[0]

        ranking_to_insert = []
        count = 0
    except Exception as e:
        print("can't get existing players: ", e)

    try: 
        for index,row in  df.iterrows():
            if index > 199:
                break
            insert_tuple = (2000, player_id_dict[row["PLAYER NAME"]])
            ranking_to_insert.append(insert_tuple)
        print(ranking_to_insert[0:5])
        insert_query = """INSERT INTO api_target ("week", "player_id") VALUES (%s, %s)"""
        curr.executemany(insert_query, ranking_to_insert)
    except Exception as e: 
        print("can't insert player: ", e)
    conn.commit()
    conn.close()
    
except Exception as e:
    print("Couldn't conect ", e)
