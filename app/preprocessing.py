import spacy
import re

# Load spacy english model
nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Clean text using regex and spaCy:
    - Remove URLs, HTML tags
    - Lowercase, lemmatize
    - Remove stop words and punctuation
    """
    # Remove URLs and HTML tags
    text = re.sub(r"http\S+|www\S+|<.*?>", "", text)

    # Process the text with spaCy
    doc = nlp(text)

    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(tokens)