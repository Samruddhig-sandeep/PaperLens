def generate_questions(summary, keywords):

    top = [k for k, _ in keywords[:5]]

    return [

        "What is the main objective of this paper?",
        f"What role does '{top[0]}' play in this research?",
        f"How is '{top[1]}' used in the proposed approach?",
        "What methodology does the paper use?",
        "What conclusions does the paper reach?"

    ]