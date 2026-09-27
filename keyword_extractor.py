
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=10):
    """
    Extracts the top TF-IDF keywords from a document.
    """

    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),   # single words + two-word phrases
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform([text])

    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(zip(feature_names, scores))
    keyword_scores.sort(key=lambda x: x[1], reverse=True)

    return keyword_scores[:top_n]