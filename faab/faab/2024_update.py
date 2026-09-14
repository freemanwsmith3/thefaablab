import psycopg2
from psycopg2 import sql
from db import connect

# Database connection details

# Establishing the connection
conn = connect()

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
