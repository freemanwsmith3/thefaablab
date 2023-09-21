import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
# Connect to your PostgreSQL database
try:


    conn = psycopg2.connect(
        host='ec2-34-199-68-114.compute-1.amazonaws.com',
        user='oibdolfaruxway',
        password='5983be3a6ab94c50df024487d2c3bcbab6a2eca9a8b4c594ddaf0b934a5553cc',
        database='d4qgddmcqs7su1'
    )
    curr = conn.cursor()


except Exception as e:
    print("Couldn't connect ", e)

# Base SQL query without the week condition
base_sql = """
SELECT 
    at.*, 
    ap.*, 
    AVG(ab.value) AS avg_value
FROM 
    api_bid AS ab
JOIN 
    api_target AS at ON ab.target_id = at.id
JOIN
    api_player AS ap ON at.player_id = ap.id
WHERE 
    ab.week = %s
GROUP BY 
    at.id, ap.id
ORDER BY 
    avg_value DESC
LIMIT 3;
"""

# Iterate from week 2 to week 13
top_arr = []
cost_arry = []
weekly_sum = 0 
weekly_cost = 0
for week in range(2, 15):
    top_arr.append(weekly_sum/5)
    cost_arry.append(weekly_cost/5)
    weekly_sum = 0 
    weekly_cost = 0
    df = pd.read_sql(base_sql, conn, params=[week])  # Use params for SQL parameter substitution

    # Assuming you want to print names for each week's results
    print(f"Week {week} Names:")
    for index, row in df.iterrows():

        player_name = row['name']
        cost = row['avg_value']
        
        
        # Read the CSV into a DataFrame
        df = pd.read_csv('2022_year_scores.csv')

        # Replace '-' with 0 (leaving 'BYE' intact)
        df.replace('-', 0, inplace=True)

        # Convert columns 6 through 21 to float where possible
        # For 'BYE' entries, we'll set them to NaN temporarily for accurate average calculation
        for col in df.columns[3 + week :21]:  # indices 5 to 20 for columns 6 to 21 (0-based)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        try: 
            # Find the row corresponding to the specified player name
            player_row = df[df['Player'] == player_name]

            # Extract columns 6 through 21 and compute the average
            # The mean method will automatically skip NaN values (which represent 'BYE' in our case)
            average_value = player_row.iloc[:, 3 + week:21].mean(axis=1).values[0]
            weekly_sum = average_value + weekly_sum

            weekly_cost = cost + weekly_cost
            
            
            print(f"Average value for {player_name} starting after week {week} is {average_value:.2f} at a cost of: {cost}")
        except:
            continue

scores_arry = top_arr[1:]

# Get the adjusted indices (index + 2)
indices = [i for i in range(2, len(scores_arry) +2)]
conn.close()
# Create a figure and axis
fig, ax1 = plt.subplots()

# Plot the numbers on the first y-axis
ax1.plot(indices, scores_arry, color='b', label='Numbers')
ax1.set_xlabel('Upcoming Week')
ax1.set_ylabel('Average pts After Acquisition', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a second y-axis
ax2 = ax1.twinx()
# Plot the cost array on the second y-axis
ax2.plot(indices, cost_arry[1:], color='r', label='Avg. FAAB %')
ax2.set_ylabel('FAAB% Spent', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add a title
plt.title("Avg. Weekly pts vs. FAAB% Spent on top 3 pick ups")

# Show the plot
plt.show()





# Close the connection
conn.close()


# # View the DataFrame
