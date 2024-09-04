import requests
from bs4 import BeautifulSoup
import re
import random
from tqdm import tqdm

# Returns 10 Working Links To News Articles About The Stock - query = stock ticker
def fetch_google_news(query, limit=10):
    print("Fetching news for:", query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Construct the search URL
    url = f"https://news.google.com/search?q={query}%20stock%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
    
    # Send a request to the Google search page
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the script with the specific class
    script = soup.find('script', class_='ds:2')
    
    if not script:
        print("Script tag with class 'ds:2' not found")
        return []
    
    # Parsing the data array from the script tag
    start_marker = 'data:'
    end_marker = ', sideChannel'

    start_index = script.string.find(start_marker) + len(start_marker)
    end_index = script.string.find(end_marker)

    # Extract the data array substring
    data_array = script.string[start_index:end_index]

    # Regular expression pattern
    pattern = r'\],null,"https://[^"]*"'

    # Find all matches
    matches = re.findall(pattern, data_array)

    cleaned_matches = list(set([match[8:-1] for match in matches]))

    # Check if the matches are working urls
    print("Initial URL List Length: ", len(cleaned_matches))
    working_links = []

    # Iterate through the random URLs with a progress bar
    str = f"Checking URLs for {query}"
    for url in tqdm(cleaned_matches, desc=str):
        try:
            response2 = requests.get(url, headers=headers, timeout=8)
            if response2.status_code == 200:
                working_links.append(url)
        except requests.exceptions.Timeout:
            print(f"Timeout occurred while trying to fetch {url}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    print("Final URL List Length: ", len(working_links))

    random_urls = random.sample(working_links, min(limit, len(working_links)))

    return random_urls

# Example usage:
# query = "AAPL"  # Replace with your search query
# news_articles = fetch_google_news(query)

# for idx, link in enumerate(news_articles):
#     print(f"{idx + 1}. {link}")
