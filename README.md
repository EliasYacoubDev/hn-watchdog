# HN Watchdog   
**Real-Time Hacker News Sentiment Monitoring with Slack Alerts**  

HN Watchdog is a **real-time sentiment analysis pipeline** that monitors Hacker News comments for a given keyword, processes them with **spaCy + RoBERTa**, and sends **Slack alerts** if a negative comment is detected.  
It also exposes a **FastAPI REST API** with Swagger documentation for querying sentiment directly.

---

## Features
- **Hacker News Ingestion** – Fetch latest comments for a keyword using the HN API.
- **Text Preprocessing** – Clean and normalize text with regex + spaCy.
- **Sentiment Analysis** – Classify comments using `cardiffnlp/twitter-roberta-base-sentiment`.
- **Model Comparison** – Optional support for `distilbert-base-uncased-finetuned-sst-2-english`.
- **Slack Alerts** – Automatically send alerts for negative sentiment comments.
- **FastAPI API** – Query sentiment for any keyword via `/sentiment` endpoint.
- **Swagger UI** – Interactive API docs available at `/docs`.
- **GitHub Actions CI** – Runs linting & tests on every push.

---

## Model Comparison

| Feature                  | RoBERTa (`cardiffnlp/twitter-roberta-base-sentiment`) | DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`) |
|--------------------------|-------------------------------------------------------|----------------------------------------------------------------|
| **Training Domain**      | Social media (Twitter) – slang, abbreviations, informal tone | General SST-2 dataset – movie reviews, formal text |
| **Sentiment Labels**     | Negative, Neutral, Positive                           | Negative, Positive (no Neutral class) |
| **Speed**                | Slightly slower (larger model)                        | Faster (distilled model) |
| **Context Understanding**| Stronger at short, noisy text                         | Better for well-formed sentences |
| **Neutral Detection**    | ✅ Yes                                                 | ❌ No |
| **Confidence Scores**    | Calibrated for short-form text                        | Calibrated for general sentences |

**Why we chose RoBERTa**  
Since Hacker News comments often resemble social media conversations — short, informal, sometimes sarcastic — RoBERTa trained on **Twitter sentiment data** performs better at detecting nuances, especially **neutral** sentiment, which SST-2 lacks.  

We keep SST-2 DistilBERT as an **optional alternative** if speed is more important than accuracy for certain deployments.

---

## Installation

### Clone the Repository
git clone https://github.com/YOUR_USERNAME/hn-watchdog.git
cd hn-watchdog
### Create a Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
### Install Dependencies
pip install -r requirements.txt
### Download spaCy Model
python -m spacy download en_core_web_sm
## Environment Variables
Create a .env file in the root:
.env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/YYYY/ZZZZ
## Running the API
Start FastAPI with:
uvicorn app.main:app --reload
Swagger Docs: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

### Example API Request
curl -X GET "http://127.0.0.1:8000/sentiment?keyword=OpenAI" -H "accept: application/json"
Response:
[
  {
    "author": "johndoe",
    "story_title": "OpenAI launches GPT-5",
    "story_url": "https://news.ycombinator.com/item?id=123456",
    "raw_text": "This is amazing!",
    "sentiment": "positive",
    "confidence": 0.984
  }
]
### Slack Alert Example
If a comment has negative sentiment:
Negative Comment Detected!
Author: johndoe
Story: Tesla faces lawsuits
Comment: This company is a disaster.
Sentiment: negative (0.92)
Read more: https://news.ycombinator.com/item?id=123456
## GitHub Actions CI/CD
Located in .github/workflows/ci.yml, the pipeline:

Installs dependencies

Runs lint checks with flake8

Runs basic import & model tests

Fails if syntax or dependency issues are found

Trigger: On every push or pull_request.

## Future Improvements
Support multiple data sources (Twitter, Reddit, TrustPilot)

Add database storage for comment history

Add speech input via Whisper or Vosk

Build a Streamlit dashboard for live monitoring
