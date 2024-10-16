import requests
from bs4 import BeautifulSoup
import re
import os
import time

# Create a directory to save the articles if it doesn't exist
os.makedirs('arxiv_articles', exist_ok=True)

# URL of the page containing the 500 articles
url = 'https://arxiv.org/list/cs.AI/recent?skip=0&show=500'

# Fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Regular expression to match the article HTML links
pattern = re.compile(r'https://arxiv.org/html/\d+\.\d+(v\d+)?')

# Find all 'a' tags with the text 'html' and href matching the pattern
links = soup.find_all('a', href=pattern, text='html')

# Get the first 300 article links
article_links = links[:300]

# Iterate over the links and download each article
for index, link in enumerate(article_links, start=1):
    article_url = link['href']
    print(f'Downloading article {index}: {article_url}')

    # Fetch the article HTML page
    article_response = requests.get(article_url)
    article_response.raise_for_status()

    # Extract the article code from the URL for naming
    article_code = article_url.split('/')[-1]

    # Save the HTML content to a file
    file_path = os.path.join('arxiv_articles', f'{article_code}.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(article_response.text)

    # Optional: Wait a short time to be polite to the server
    time.sleep(1)

print('Finished downloading 300 articles.')