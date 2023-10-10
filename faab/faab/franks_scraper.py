import requests
from bs4 import BeautifulSoup
import csv

sites= ['http://www.cfbstats.com/2023/leader/national/team/offense/split01/category25/sort01.html', 'http://www.cfbstats.com/2023/leader/national/team/defense/split01/category25/sort01.html','http://www.cfbstats.com/2023/leader/national/team/offense/split01/category27/sort01.html','http://www.cfbstats.com/2023/leader/national/team/defense/split01/category27/sort01.html','http://www.cfbstats.com/2023/leader/national/team/offense/split01/category30/sort01.html','http://www.cfbstats.com/2023/leader/national/team/defense/split01/category30/sort01.html','http://www.cfbstats.com/2023/leader/national/team/offense/split01/category21/sort01.html','http://www.cfbstats.com/2023/leader/national/team/defense/split01/category21/sort01.html']
i = 0
for url in sites:
    i +=1
    # Fetching the HTML content

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding the table
    table = soup.find('table', class_='leaders')

    # Extracting header data
    headers = []
    for th in table.find('tr').find_all('th'):
        headers.append(th.get_text(strip=True))

    # Extracting row data
    rows = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        rowData = []
        for td in row.find_all('td'):
            if td.a:  # Check if there's a link in the cell and get its text
                rowData.append(td.a.get_text(strip=True))
            else:
                rowData.append(td.get_text(strip=True))
        rows.append(rowData)

    # Writing data to CSV
    with open(f'leaders_data_{i}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)

    print("Data written to 'leaders_data.csv'")
