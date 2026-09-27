
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

@st.cache_resource
def load_nltk_resources():
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]

    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    return lemmatizer, stop_words

lemmatizer, stop_words = load_nltk_resources()

def preprocess_text(text):
    tokens = word_tokenize(text)

    cleaned_tokens = []

    for token in tokens:
        token = token.lower()

        if token.isalpha() and token not in stop_words:
            cleaned_tokens.append(lemmatizer.lemmatize(token))

    cleaned_text = " ".join(cleaned_tokens)

    return cleaned_text, cleaned_tokens