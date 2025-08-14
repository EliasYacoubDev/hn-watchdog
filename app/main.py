from fastapi import FastAPI, Query
from app.comments_ingest import fetch_hn_comments
from app.preprocessing import clean_text
from app.sentiment_model_RoBERTa import classify_sentiment
from app.alerting import send_slack_alert

app = FastAPI(title="Real-Time Sentiment Analysis API")

@app.get("/sentiment")
def get_sentiment(query: str = Query(..., description="Search keyword"),
                  limit: int = Query(5, description="Number of comments to fetch")):
    """
    Fetch Hacker News comments, preprocess them, and return sentiment analysis.
    """
    comments = fetch_hn_comments(query, limit)
    results = []
    for c in comments:
        cleaned_text = clean_text(c["text"])
        sentiment = classify_sentiment(cleaned_text)
        comment_result = {
            "created_at": c["created_at"],
            "author": c["author"],
            "story_title": c["story_title"],
            "story_url": c["story_url"],
            "raw_text": c["text"],
            "cleaned_text": cleaned_text,
            "sentiment": sentiment["sentiment"],
            "confidence": sentiment["confidence"]
        }
        results.append(comment_result)
        # Send Slack alert if negative and high confidence
        if sentiment["sentiment"] == "negative" and sentiment["confidence"] >= 0.7:
            send_slack_alert(comment_result)
    return {"query": query, "count": len(results), "results": results}
