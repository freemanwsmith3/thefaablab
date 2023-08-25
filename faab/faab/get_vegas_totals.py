import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.vegasinsider.com/nfl/odds/most-passing-yards/"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='odds-table game-table')
stats = {}
specific_stats = {}
player_name = ''
# If the table exists, get the desired data
if table:
    td_elements = table.find_all('td')
    for td in td_elements:
        span = td.find('span')
        if span:
            
            if span.text.strip()[0] !=  'o':
                stats[player_name] = specific_stats
                player_name = span.text.strip()
                stats[player_name] = None
            elif stats[player_name] is None:
                specific_stats = {}
                specific_stats['passing_yards'] = float(span.text.strip()[1:])
                
            else: 
                continue

else:
    print("Couldn't find the table.")


url = "https://www.vegasinsider.com/nfl/odds/most-passing-touchdowns/"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='odds-table game-table')
# If the table exists, get the desired data
specific_stats = {}
if table:
    td_elements = table.find_all('td')
    for td in td_elements:
        span = td.find('span')
        if span:
            if span.text.strip()[0] !=  'o':
                player_name = span.text.strip()
                if stats.get(player_name):
                    stats[player_name]['passing_tds'] = 'none'
                else: 
                    stats[player_name] = {}
                    stats[player_name]['passing_tds'] = 'none'
            elif stats[player_name] and stats[player_name]['passing_tds'] == 'none':
                specific_stats=stats[player_name]
                specific_stats['passing_tds'] = float(span.text.strip()[1:])
                stats[player_name] = specific_stats
            else: 
                continue


url = "https://www.vegasinsider.com/nfl/odds/most-rushing-yards/"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='odds-table game-table')
# If the table exists, get the desired data
specific_stats = {}
if table:
    td_elements = table.find_all('td')
    for td in td_elements:
        span = td.find('span')
        if span:
            if span.text.strip()[0] !=  'o':
                player_name = span.text.strip()
                if stats.get(player_name):
                    stats[player_name]['rushing_yards'] = 'none'
                else: 
                    stats[player_name] = {}
                    stats[player_name]['rushing_yards'] = 'none'
            elif stats[player_name] and stats[player_name]['rushing_yards'] == 'none':
                specific_stats=stats[player_name]
                specific_stats['rushing_yards'] = float(span.text.strip()[1:])
                stats[player_name] = specific_stats
            else: 
                continue

####
url = "https://www.vegasinsider.com/nfl/odds/most-receiving-touchdowns"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='odds-table game-table')
# If the table exists, get the desired data
specific_stats = {}

if table:
    td_elements = table.find_all('td')
    for td in td_elements:
        span = td.find('span')
        if span:
            if span.text.strip()[0] !=  'o':
                player_name = span.text.strip()
                if stats.get(player_name):
                    stats[player_name]['receiving_tds'] = 'none'
                else: 
                    stats[player_name] = {}
                    stats[player_name]['receiving_tds'] = 'none'
            elif stats[player_name] and stats[player_name]['receiving_tds'] == 'none':
                specific_stats=stats[player_name]
                specific_stats['receiving_tds'] = float(span.text.strip()[1:])
                stats[player_name] = specific_stats
            else: 
                continue



####
url = "https://www.vegasinsider.com/nfl/odds/most-receiving-yards"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='odds-table game-table')
# If the table exists, get the desired data
specific_stats = {}

if table:
    td_elements = table.find_all('td')
    for td in td_elements:
        span = td.find('span')
        if span:
            if span.text.strip()[0] !=  'o':
                player_name = span.text.strip()
                if stats.get(player_name):
                    stats[player_name]['receiving_yards'] = 'none'
                else: 
                    stats[player_name] = {}
                    stats[player_name]['receiving_yards'] = 'none'
            elif stats[player_name] and stats[player_name]['receiving_yards'] == 'none':
                specific_stats=stats[player_name]
                specific_stats['receiving_yards'] = float(span.text.strip()[1:])
                stats[player_name] = specific_stats
            else: 
                continue

projections = {}
projections['Davante Adams'] = 175.95
for player in stats:
    total = 0
    rec_yards = False
    rec_tds = False
    if player == 'Travis Kelce' or player == 'T.J. Hockenson' or player == 'Dawson Knox':
        continue 
    print(stats.get(player))
    try:
        for key in stats.get(player):

            print(key)
            print(stats[player][key])
            if key == 'receiving_yards':
                total = stats[player][key]*.1 + total
                rec_yards = True
            if key == 'receiving_tds':
                total = stats[player][key]*6 + total
                rec_tds = True
            if rec_yards == True and rec_tds == True:
                projections[player] = round(total, 2)
    
    except Exception as e:
        print(e) 
        continue
    print('------------')
sorted_projections = dict(sorted(projections.items(), key=lambda item: item[1], reverse=True))

df = pd.DataFrame(list(sorted_projections.items()), columns=["Player", "Vegas Projections"])
df.to_csv('wrs_vegas_odds')