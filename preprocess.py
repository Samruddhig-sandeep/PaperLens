
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download resources (runs only once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    """
    Cleans the extracted text using NLP preprocessing.
    Returns cleaned text and tokens.
    """

    # Lowercase
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Remove punctuation and stopwords
    tokens = [
        word for word in tokens
        if word not in stop_words
        and word not in string.punctuation
        and word.isalpha()
    ]

    # Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    cleaned_text = " ".join(tokens)

    return cleaned_text, tokens