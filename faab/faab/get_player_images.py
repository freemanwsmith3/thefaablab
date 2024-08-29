import psycopg2
import requests
from bs4 import BeautifulSoup

# Function to strip suffixes from player names
def strip_suffix(name):
    suffixes = ["sr", "jr", "ii", "iii", "iv", "v", "sr.", "jr.", "ii.", "iii.", "iv.", "v."]
    name_parts = name.split()
    if len(name_parts) > 2 and name_parts[-1].lower() in suffixes:
        name_parts = name_parts[:-1]  # Remove the suffix
    return " ".join(name_parts)

# Function to construct NFL player URL
def construct_url(player_name):
    player_name = strip_suffix(player_name)
    name_parts = player_name.lower().split()
    return f"https://www.nfl.com/players/{'-'.join(name_parts)}/"

# Function to scrape the player's image URL
def get_player_image_url(player_name):
    url = construct_url(player_name)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the meta tag with property 'og:image'
        meta_tag = soup.find("meta", property="og:image")
        if meta_tag:
            return meta_tag["content"]
        else:
            return f"No og:image found for {player_name}"
    else:
        return f"Failed to retrieve page for {player_name}. Status code: {response.status_code}"

# Function to fetch the first five players from the database
def fetch_first_five_players_from_db():
    conn = psycopg2.connect(
        host='ec2-52-71-90-133.compute-1.amazonaws.com',
        user='yscnkbjrdccjdm',
        password='abc2e73db2c853ef565d543fe31c401b2f0be626920e7707b705302f6bf519be',
        database='deranomlqt3v7k'
    )
    curr = conn.cursor()
    curr.execute("SELECT id, name FROM api_player")
    players = curr.fetchall()
    curr.close()
    conn.close()
    return players

# Function to update player image URL in the database
def update_player_image_url(player_id, image_url):
    # Check if the image URL ends with .svg
    if image_url.lower().endswith('.svg'):
        print(f"Skipping update for player ID {player_id} due to SVG image format.")
        return  # Skip the update if the image is an SVG

    conn = psycopg2.connect(
        host='ec2-52-71-90-133.compute-1.amazonaws.com',
        user='yscnkbjrdccjdm',
        password='abc2e73db2c853ef565d543fe31c401b2f0be626920e7707b705302f6bf519be',
        database='deranomlqt3v7k'
    )
    curr = conn.cursor()
    curr.execute(
        "UPDATE api_player SET image = %s WHERE id = %s",
        (image_url, player_id)
    )
    conn.commit()
    curr.close()
    conn.close()

# Main scraping function
def scrape_player_images_and_update_db():
    players = fetch_first_five_players_from_db()
    for player_id, player_name in players:
        image_url = get_player_image_url(player_name)
        update_player_image_url(player_id, image_url)
        print(f"Processed {player_name} with image URL: {image_url}")

if __name__ == "__main__":
    scrape_player_images_and_update_db()
