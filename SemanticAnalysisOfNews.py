from GetNewsTitles import fetch_google_news
from GetStockMarketNews import get_stock_market_news
from tqdm import tqdm
from NewsPredictorFunction import get_sentiment_score
from SummarizeText import summarize_text

#venv\Scripts\activate

def keep_first_n_words(text, n=500):
    """
    Keeps only the first n words of the input text.

    Parameters:
    - text (str): The input text.
    - n (int): The number of words to keep. Default is 500.

    Returns:
    - truncated_text (str): The text with only the first n words.
    """
    # Split the text into words
    words = text.split()
    
    # Keep only the first n words
    first_n_words = words[:n]
    
    # Join the words back into a single string
    truncated_text = ' '.join(first_n_words)
    
    return truncated_text

print("\n\nFinding news articles for the search query...")
query = "AAPL"  # Replace with your search query
news_articles = fetch_google_news(query, limit=40)   # Returns a list of 10 news articles

print("\n\nFinding news contents for the articles...")
results = []
shallow_results = []
for idx, link in tqdm(enumerate(news_articles), desc="Fetching news contents"):
    stockDetails = get_stock_market_news(link, query, idx)
    if stockDetails is not None and len(stockDetails) > 200:
        ### Summarize the news content:
        print("Summarizing Text")
        summarize = summarize_text(keep_first_n_words(stockDetails, n=350))
        print(summarize)
        results.append(get_sentiment_score(summarize))

        print("Saving")
        shallow_results.append(get_sentiment_score(keep_first_n_words(stockDetails, n=300)))

print("\n\nResults:")
print(results)
print("\n\nShallow Results:")
print(shallow_results)
