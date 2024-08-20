# Importing the required libraries
from xml.etree.ElementTree import QName
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
from slugify import slugify


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


    df = pd.read_csv('./faab/faab/stats/2024rankings.csv')

    # Create a new column 'in_set' which is True if the player's name is in 'my_set' and False otherwise
    for index,row in  df.iterrows():
        name = row['PLAYER NAME']
        rank = index 
    curr.execute("""SELECT * FROM api_player""")
    players = curr.fetchall()
    player_id_dict = {}
    for player in players:
        player_id_dict[player[1]] = player[0]

    ranking_to_insert = []
    count = 0
    for index,row in  df.iterrows():
        if index > 199:
            break
        insert_tuple = (1000, player_id_dict[row["PLAYER NAME"]])
        ranking_to_insert.append(insert_tuple)
    print(ranking_to_insert[0:5])
    insert_query = """INSERT INTO api_target ("week", "player_id") VALUES (%s, %s)"""
    curr.executemany(insert_query, ranking_to_insert)
    conn.commit()
    conn.close()
    
except Exception as e:
    print("Couldn't conect ", e)
