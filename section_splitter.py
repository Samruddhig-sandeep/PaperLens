import re

HEADINGS = [
    "abstract",
    "introduction",
    "methodology",
    "methods",
    "results",
    "discussion",
    "conclusion",
    "references"
]

def split_sections(text):

    sections = {}

    lower = text.lower()

    for i, heading in enumerate(HEADINGS):

        match = re.search(rf"\\b{heading}\\b", lower)

        if not match:
            continue

        start = match.start()

        end = len(text)

        for next_heading in HEADINGS[i+1:]:

            next_match = re.search(rf"\\b{next_heading}\\b", lower[start+1:])

            if next_match:

                end = start + 1 + next_match.start()

                break

        sections[heading.title()] = text[start:end].strip()

    return sections