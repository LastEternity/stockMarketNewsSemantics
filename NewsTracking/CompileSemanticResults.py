from collections import Counter
from SemanticAnalysisOfNews import fetch_and_analyze_news

def analyze_sentiment(results, shallow_results):
    """
    Analyzes the sentiment results to determine if the stock is performing well.

    Parameters:
    - results (list): List of sentiment results from the summarized text.
    - shallow_results (list): List of sentiment results from the truncated text.

    Returns:
    - aggregated_results (dict): Aggregated sentiment scores for both results and shallow_results.
    - overall_sentiment (dict): Overall sentiment based on aggregated scores.
    """
    def aggregate_sentiments(sentiments):
        """
        Aggregates sentiment scores from a list of results.
        """
        labels = []
        scores = []
        
        # Extract labels and scores
        for sublist in sentiments:
            if isinstance(sublist, list):
                for item in sublist:
                    if isinstance(item, dict):
                        labels.append(item.get('label'))
                        scores.append(item.get('score'))
        
        label_counts = Counter(labels)
        average_scores = {label: sum(score for lbl, score in zip(labels, scores) if lbl == label) / label_counts[label]
                          for label in label_counts}
        return average_scores
    
    def determine_sentiment(score_dict):
        """
        Determines the overall sentiment based on average scores.
        """
        positive_score = score_dict.get('positive', 0)
        negative_score = score_dict.get('negative', 0)
        neutral_score = score_dict.get('neutral', 0)
        
        if positive_score > max(negative_score, neutral_score):
            return 'Positive'
        elif negative_score > max(positive_score, neutral_score):
            return 'Negative'
        else:
            return 'Neutral'

    # Aggregate sentiments
    aggregated_results = {
        'results': aggregate_sentiments(results),
        'shallow_results': aggregate_sentiments(shallow_results)
    }
    
    # Determine overall sentiment
    overall_sentiment = {
        'results': determine_sentiment(aggregated_results['results']),
        'shallow_results': determine_sentiment(aggregated_results['shallow_results'])
    }
    
    return aggregated_results, overall_sentiment

def run_queries(queries, num_articles=40):
    """
    Runs sentiment analysis on news articles for each query.

    Parameters:
    - queries (list): List of stock queries.
    - num_articles (int): Number of articles to fetch for each query.
    """
    for query in queries:
        print(f"\n\nAnalyzing news for '{query}'...")
        results, shallow_results = fetch_and_analyze_news(query, limit=num_articles)  # Make sure fetch_and_analyze_news uses query

        aggregated_results, overall_sentiment = analyze_sentiment(results, shallow_results)

        print("Aggregated Results:")
        print(aggregated_results)
        print("\nOverall Sentiment:")
        print(overall_sentiment)

        # Save the results to a file
        with open(f"SemanticResults/{query}_results.txt", "w") as file:
            file.write(f"Aggregated Results:\n{aggregated_results}\n\nOverall Sentiment:\n{overall_sentiment}")

        with open(f"SemanticResults/{query}_specific_results.txt", "w") as file:
            file.write(f"Summary Results:\n{results}\n\nShallow Results:\n{shallow_results}")

# Run the analysis for specified queries
run_queries(["GOOGLE", "APPLE", "MICROSOFT", "AMAZON", "FACEBOOK"], num_articles=10)
