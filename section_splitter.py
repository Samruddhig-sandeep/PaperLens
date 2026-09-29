import re


SECTION_NAMES = [
    "abstract",
    "introduction",
    "background",
    "related work",
    "literature review",
    "methodology",
    "method",
    "methods",
    "materials and methods",
    "experimental setup",
    "experiments",
    "results",
    "results and discussion",
    "discussion",
    "conclusion",
    "future work",
    "limitations",
    "acknowledgements",
    "acknowledgments",
    "references"
]


def clean_heading(heading):
    """
    Remove numbering and punctuation from a detected heading.
    """

    heading = heading.strip()

    heading = re.sub(
        r"^(?:\d+(?:\.\d+)*[\.\):]?\s*)",
        "",
        heading
    )

    heading = re.sub(
        r"^(?:[IVXLCDM]+[\.\):]\s*)",
        "",
        heading,
        flags=re.IGNORECASE
    )

    return heading.strip()


def split_sections(text):

    sections = {}

    if not text or not text.strip():
        return sections

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = text.split("\n")

    detected = []

    # ---------------------------------------------------------
    # METHOD 1:
    # Look for headings that occupy their own line
    # ---------------------------------------------------------

    for i, line in enumerate(lines):

        clean_line = re.sub(r"\s+", " ", line.strip())

        if not clean_line:
            continue

        normalized = clean_heading(clean_line).lower()

        # Remove trailing punctuation
        normalized = normalized.rstrip(" .:;-")

        if normalized in SECTION_NAMES:

            detected.append(
                (i, clean_line)
            )

            continue

        # -----------------------------------------------------
        # Numbered headings
        # Examples:
        # 1 Introduction
        # 1. Introduction
        # 2.1 Methodology
        # I. Introduction
        # -----------------------------------------------------

        numbered = re.match(
            r"^(?:"
            r"\d+(?:\.\d+)*[\.\):]?"
            r"|"
            r"[IVXLCDM]+[\.\):]"
            r")\s+(.+)$",
            clean_line,
            re.IGNORECASE
        )

        if numbered:

            heading_text = numbered.group(1).strip()
            normalized_heading = heading_text.lower().rstrip(
                " .:;-"
            )

            if normalized_heading in SECTION_NAMES:

                detected.append(
                    (i, clean_line)
                )


    # ---------------------------------------------------------
    # METHOD 2:
    # If line-based detection failed, search the entire text.
    #
    # This handles PDFs where headings are extracted strangely.
    # ---------------------------------------------------------

    if not detected:

        flat_text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        for section_name in SECTION_NAMES:

            pattern = re.compile(
                rf"(?<![A-Za-z])"
                rf"(?:"
                rf"\d+(?:\.\d+)*[\.\):]?\s*"
                rf"|"
                rf"[IVXLCDM]+[\.\):]\s*"
                rf")?"
                rf"{re.escape(section_name)}"
                rf"(?![A-Za-z])",
                re.IGNORECASE
            )

            match = pattern.search(flat_text)

            if match:

                # Find approximate position in original text
                original_match = re.search(
                    re.escape(match.group()),
                    text,
                    re.IGNORECASE
                )

                if original_match:

                    before = text[:original_match.start()]
                    line_number = before.count("\n")

                    detected.append(
                        (
                            line_number,
                            match.group().strip()
                        )
                    )


    # ---------------------------------------------------------
    # Remove duplicate headings
    # ---------------------------------------------------------

    unique = []

    seen = set()

    for position, heading in detected:

        clean = clean_heading(heading)

        key = clean.lower()

        if key not in seen:

            seen.add(key)

            unique.append(
                (position, heading)
            )


    # Sort according to document position
    unique.sort(key=lambda x: x[0])


    # ---------------------------------------------------------
    # Extract section content
    # ---------------------------------------------------------

    for index, (start_line, heading) in enumerate(unique):

        if index + 1 < len(unique):

            end_line = unique[index + 1][0]

        else:

            end_line = len(lines)


        content = "\n".join(
            lines[start_line:end_line]
        ).strip()


        display_heading = clean_heading(heading)

        if display_heading:

            sections[display_heading.title()] = content


    return sections