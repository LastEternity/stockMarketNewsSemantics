from GetNewsTitles import fetch_google_news
from GetStockMarketNews import get_stock_market_news
from tqdm import tqdm
from NewsPredictorFunction import get_sentiment_score
from SummarizeText import summarize_text

def keep_first_n_words(text, n=500):
    """
    Keeps only the first n words of the input text.

    Parameters:
    - text (str): The input text.
    - n (int): The number of words to keep. Default is 500.

    Returns:
    - truncated_text (str): The text with only the first n words.
    """
    words = text.split()
    first_n_words = words[:n]
    truncated_text = ' '.join(first_n_words)
    return truncated_text

def fetch_and_analyze_news(query, limit=40):
    """
    Fetches news articles based on the query, analyzes their content, and returns the results.

    Parameters:
    - query (str): The search query for fetching news articles.
    - limit (int): The number of news articles to fetch. Default is 40.

    Returns:
    - results (list): List of sentiment scores from the summarized text.
    - shallow_results (list): List of sentiment scores from the truncated text.
    """
    print("\n\nFinding news articles for the search query...")
    news_articles = fetch_google_news(query, limit=limit)  # Fetches news articles

    print("\n\nFinding news contents for the articles...")
    results = []
    shallow_results = []
    
    for idx, link in tqdm(enumerate(news_articles), desc="Fetching news contents"):
        stockDetails = get_stock_market_news(link, query, idx)
        if stockDetails is not None and len(stockDetails) > 200:
            try:
                print("Summarizing Text")
                summarize = summarize_text(keep_first_n_words(stockDetails, n=350))
                print(summarize)
                results.append(get_sentiment_score(summarize))
            except Exception as e:
                print(f"Error in summarizing text: {e}")

            print("Saving")
            shallow_results.append(get_sentiment_score(keep_first_n_words(stockDetails, n=300)))

    print("\n\nResults:")
    print(results)
    print("\n\nShallow Results:")
    print(shallow_results)
    
    return results, shallow_results

# Example usage
# query = "AAPL"  # Replace with your search query
# results, shallow_results = fetch_and_analyze_news(query)