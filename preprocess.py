
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources if missing
required_resources = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/stopwords", "stopwords"),
    ("corpora/wordnet", "wordnet"),
    ("corpora/omw-1.4", "omw-1.4"),
]

for path, resource in required_resources:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    tokens = word_tokenize(text)

    cleaned_tokens = []

    for token in tokens:
        token = token.lower()

        if token.isalpha() and token not in stop_words:
            cleaned_tokens.append(lemmatizer.lemmatize(token))

    cleaned_text = " ".join(cleaned_tokens)

    return cleaned_text, cleaned_tokens