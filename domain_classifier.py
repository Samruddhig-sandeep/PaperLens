
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

@st.cache_resource
def load_domain_model():

    df = pd.read_csv("training_data.csv")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        lowercase=True,
        ngram_range=(1,2),
        max_features=3000
    )

    X = vectorizer.fit_transform(df["text"])

    model = MultinomialNB()
    model.fit(X, df["label"])

    return vectorizer, model

vectorizer, model = load_domain_model()

def predict_domain(text):

    vec = vectorizer.transform([text])

    label = model.predict(vec)[0]

    confidence = model.predict_proba(vec).max() * 100

    return label, round(confidence,1)