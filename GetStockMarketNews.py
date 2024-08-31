import os
import requests
from bs4 import BeautifulSoup

def get_stock_market_news(url, query, num):
    try:
        response = requests.get(url, timeout=8)
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to fetch {url}")
        return ""
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""
    
    if response.status_code == 200:
        # Proceed with parsing the content if needed
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all paragraphs as news headlines
        news_headlines = [headline.text for headline in soup.find_all('p')]
        
        # Ensure the 'files' directory exists
        os.makedirs('files', exist_ok=True)

        # Save headlines to a file in the 'files' subfolder with a dynamic filename
        filename = f"files/headlines_{query}_{num}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            for headline in news_headlines:
                file.write(headline + "\n")
        
        toReturn = ""
        for i in range(len(news_headlines)):
            toReturn += news_headlines[i] + "\n"
        return toReturn
    else:
        print("Failed to fetch stock market news. Status code:", response.status_code)