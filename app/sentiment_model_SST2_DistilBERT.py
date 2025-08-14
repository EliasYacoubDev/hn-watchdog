from transformers import pipeline

# Load model once
sentiment_pipeline = pipeline("sentiment-analysis")

def classify_sentiment(text, max_length=512):
    """
    Classify sentiment for a single text string.
    Returns dict: {sentiment, confidence}
    """
    result = sentiment_pipeline(text[:max_length])[0]
    return {
        "sentiment": result["label"].lower(),
        "confidence": round(result["score"], 4)
    }
