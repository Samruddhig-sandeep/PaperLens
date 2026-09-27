
def compare_papers(
    meta1, meta2,
    domain1, domain2,
    extractive1, extractive2,
    abstractive1, abstractive2,
    keywords1, keywords2,
    stats1, stats2
):

    return {
        "Paper A": {
            "Title": meta1["title"],
            "Year": meta1["year"],
            "Domain": domain1,
            "Words": stats1["Words"],
            "Reading Time": stats1["Reading Time"],
            "Keywords": ", ".join([k for k, _ in keywords1[:5]]),
            "Extractive": extractive1,
            "Abstractive": abstractive1
        },
        "Paper B": {
            "Title": meta2["title"],
            "Year": meta2["year"],
            "Domain": domain2,
            "Words": stats2["Words"],
            "Reading Time": stats2["Reading Time"],
            "Keywords": ", ".join([k for k, _ in keywords2[:5]]),
            "Extractive": extractive2,
            "Abstractive": abstractive2
        }
    }