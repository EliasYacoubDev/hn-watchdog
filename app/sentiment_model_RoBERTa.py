from transformers import pipeline

# Load RoBERTa 3-class sentiment model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def classify_sentiment(text, max_length=512):
    """
    Classify sentiment for a single text string.
    Returns dict: {sentiment, confidence}
    """
    result = sentiment_pipeline(text[:max_length])[0]
    return {
        "sentiment": result["label"].lower(),   # positive / neutral / negative
        "confidence": round(result["score"], 4)
    }
