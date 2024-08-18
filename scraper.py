import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def parse_html(html):
    if not html:
        print('No HTML content to parse.')
        return [], []
    
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    
    # Example: Extracting data from a table
    table = soup.find('table')  # Find the first table
    if not table:
        print('No table found in the HTML.')
        return [], []

    headers = [header.text for header in table.find_all('th')]  # Extract headers
    rows = table.find_all('tr')  # Find all rows

    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        data.append([column.text.strip() for column in columns])
    
    return headers, data

def save_to_csv(headers, data, filename):
    if not headers or not data:
        print('No data to save.')
        return
    
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(filename, index=False)

def main(url, filename):
    html = fetch_page(url)
    if html is None:
        print('Failed to retrieve the webpage.')
        return
    
    headers, data = parse_html(html)
    if headers and data:
        save_to_csv(headers, data, filename)
        print(f'Data saved to {filename}')
    else:
        print('No data to save.')

# Example usage
url = 'https://ninjatables.com/examples-of-data-table-design-on-website/'  # Replace with your target URL
filename = 'scraped_data.csv'
main(url, filename)