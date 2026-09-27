
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def generate_summary(text, sentence_count=5):
    """
    Generates a summary using the TextRank algorithm.
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()

    summary = summarizer(parser.document, sentence_count)

    return " ".join(str(sentence) for sentence in summary)