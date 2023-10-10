import requests
from bs4 import BeautifulSoup
import csv

# Sending a request to the provided URL
url = "https://www.espn.com/college-football/fpi/_/view/resume/sort/resume.fpirank/dir/asc?fbclid=IwAR0wkNzhIGX55FK0su2odOWb2uFa0DFbAJ9PtdUvQMKW1xu2huOYuvu76mg"
headers_request = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
response = requests.get(url, headers=headers_request)
soup = BeautifulSoup(response.text, 'html.parser')

# Finding the specific tables
tables = soup.findAll('table', {'class': 'Table'})

data = []
all_headers = set()
for table in tables:
    # Extracting table headers
    headers = [header.text for header in table.find('tr', {'class': 'Table__sub-header'}).findAll('th')]
    all_headers.update(headers)  # Add new headers to the set
    
    # Extracting rows
    rows = table.find('tbody').findAll('tr', {'class': 'Table__TR--sm'})

    for row in rows:
        current_row = {}
        for header, cell in zip(headers, row.findAll('td')):
            current_row[header] = cell.text.strip()
        data.append(current_row)

# Convert the set of headers to a list for the CSV writer
headers_list = list(all_headers)

# Writing the scraped data to a CSV file
filename = "scraped_data.csv"
with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers_list)
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print(f"Data from all tables has been merged and written to {filename}")