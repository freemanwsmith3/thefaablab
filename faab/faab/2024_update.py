import psycopg2
from psycopg2 import sql

# Database connection details
db_config = {
    'dbname': 'd4qgddmcqs7su1',
    'user': 'oibdolfaruxway',
    'password': '5983be3a6ab94c50df024487d2c3bcbab6a2eca9a8b4c594ddaf0b934a5553cc',
    'host': 'ec2-34-199-68-114.compute-1.amazonaws.com',
    'port': '5432'
}

# Establishing the connection
conn = psycopg2.connect(**db_config)

# Creating a cursor object
cur = conn.cursor()

# The SQL query to be executed
query = """
SELECT id, "name", team_id, position_id, link, image
FROM public.api_player;
"""

try:
    # Executing the SQL query
    cur.execute(query)
    
    # Fetching all results from the executed query
    results = cur.fetchall()
    
    # Printing the results
    for row in results:
        print(row)
except Exception as e:
    print(f"Error: {e}")
finally:
    # Closing the cursor and connection
    cur.close()
    conn.close()
