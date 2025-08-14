import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(comment_data):
    """
    Send Slack alert for a negative sentiment comment.
    """
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL is not set in environment variables.")
    
    message = (
        f"🚨 *Negative Comment Detected!*\n"
        f"*Author:* {comment_data['author']}\n"
        f"*Story:* {comment_data['story_title']}\n"
        f"*Comment:* {comment_data['raw_text']}\n"
        f"*Sentiment:* {comment_data['sentiment']} ({comment_data['confidence']})\n"
        f"<{comment_data['story_url']}|Read more>"
    )
    payload = {"text": message}
    response  = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()  # raise error if request failed
