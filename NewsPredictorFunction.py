from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

def get_sentiment_score(text):
    # Load the pre-trained model and tokenizer
    model = AutoModelForSequenceClassification.from_pretrained("KernAI/stock-news-distilbert")
    tokenizer = AutoTokenizer.from_pretrained("KernAI/stock-news-distilbert")

    # Create a pipeline for text classification
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Classify the input text and return the result
    result = classifier(text)
    return result