import requests
from bs4 import BeautifulSoup
import csv
import re

# URL to scrape
url = "https://www.hsbc.com.hk/sitemap/"
root_url = "https://www.hsbc.com.hk"

# Send a request to the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all doormat link groups
    links_groups = soup.find_all('div', class_='links-group')
    
    # Prepare data for CSV
    doormat_data = []
    
    # Extract data from each links group
    for group in links_groups:
        # Get the section heading
        heading_link = group.find('a', class_='doormat-heading-link')
        section_title = ""
        if heading_link and heading_link.find('h2', class_='doormat-heading'):
            section_title = heading_link.find('h2', class_='doormat-heading').text.strip()
        
        # Get all doormat links in this section
        doormat_links = group.find('ul', class_='doormat-links')
        if doormat_links:
            links = doormat_links.find_all('li')
            for link in links:
                a_tag = link.find('a')
                if a_tag:
                    title = a_tag.text.strip()
                    href = a_tag.get('href', '')
                    
                    # Create full URL by appending to root URL if it's a relative path
                    if href.startswith('/'):
                        full_url = root_url + href
                    else:
                        full_url = href
                    
                    # Add to our data list
                    doormat_data.append({
                        'section': section_title,
                        'title': title,
                        'url': full_url
                    })
    
    # Write data to CSV file
    csv_file = 'hsbc_doormat_links.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['section', 'title', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in doormat_data:
            writer.writerow(data)
    
    print(f"Successfully extracted {len(doormat_data)} doormat links and saved to {csv_file}")
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching the webpage: {e}")
except Exception as e:
    print(f"An error occurred: {e}")