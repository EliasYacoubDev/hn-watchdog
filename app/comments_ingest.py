import requests

BASE_URL = "https://hn.algolia.com/api/v1/search"

def fetch_hn_comments(query="Tesla", limit=10):
    params = {
        "query": query,
        "hitsPerPage": limit,
        "tags": "comment"
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json().get("hits", [])

    results = []
    for comment in data:
        text = comment.get("comment_text", "").replace("<p>", " ").replace("</p>", " ").strip()
        if text:
            results.append({
                "text": text,
                "author": comment.get("author"),
                "created_at": comment.get("created_at"),
                "story_title": comment.get("story_title"),
                "story_url": comment.get("story_url")
            })
    return results
