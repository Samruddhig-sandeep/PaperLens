import re

def get_stats(text, tokens):

    words = len(text.split())

    sentences = len(re.split(r"[.!?]+", text))

    unique = len(set(tokens))

    reading = max(1, words // 200)

    avg = round(words / sentences, 1) if sentences else 0

    return {

        "Words": words,
        "Characters": len(text),
        "Unique Words": unique,
        "Sentences": sentences,
        "Reading Time": reading,
        "Avg Sentence Length": avg

    }