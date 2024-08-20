import psycopg2
import random

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

# Query to get all players who are targets for week 27
target_query = """
SELECT DISTINCT player_id
FROM public.api_target
WHERE week = 27;
"""

cur.execute(target_query)
targets = cur.fetchall()

# Extracting player ids
player_ids = [target[0] for target in targets]

# Format player_ids for SQL IN clause
player_ids_str = ','.join(map(str, player_ids))

# Query to get the count of bids per player for week 27, sorted by count in descending order
bid_count_query = f"""
SELECT player_id, COUNT(*) as bid_count
FROM public.api_bid
WHERE week = 27 AND player_id IN ({player_ids_str})
GROUP BY player_id
ORDER BY bid_count DESC;
"""

cur.execute(bid_count_query)
bid_counts = cur.fetchall()

# Parameters for bid amount
max_bid_amount = 20
min_bid_amount = 1
num_players = len(bid_counts)
bid_step = (max_bid_amount - min_bid_amount) / (num_players - 1) if num_players > 1 else 0

# Parameters for number of bids
max_bids = 500
min_bids = 50
bid_count_step = (max_bids - min_bids) / (num_players - 1) if num_players > 1 else 0

# Function to generate a random bid amount centered around the bid_step
def generate_random_bid_amount(base_bid_amount):
    deviation = bid_step * 10
    bid_amount = random.gauss(base_bid_amount, deviation)
    # Ensure bid amount is between 1 and 100
    return int(max(1, min(100, round(bid_amount))))

# Loop through the sorted players and insert randomized bids
for i, (player_id, bid_count) in enumerate(bid_counts):
    base_bid_amount = max_bid_amount - i * bid_step
    num_bids = int(max_bids - i * bid_count_step)
    
    for _ in range(num_bids):
        bid_amount = generate_random_bid_amount(base_bid_amount)
        insert_bid_query = """
        INSERT INTO public.api_bid (value, created_at, "user", week, player_id)
        VALUES (%s, NOW(), %s, %s, %s);
        """
        cur.execute(insert_bid_query, (bid_amount, 'system', 27, player_id))
        print(f"Inserted bid: Player ID={player_id}, Bid Amount={bid_amount}")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

# Printing results
print("Inserted random bids for players for week 27 with decreasing bid amounts and counts.")
