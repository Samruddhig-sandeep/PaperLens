import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _get_client():
    """Create a Groq client when an API key is available."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


def _build_evidence(text, sections):
    """Build a focused evidence block for research-gap analysis."""

    preferred_sections = [
        "Abstract",
        "Introduction",
        "Methodology",
        "Methods",
        "Results",
        "Discussion",
        "Conclusion",
        "Future Work",
        "Limitations",
    ]

    evidence_parts = []

    if sections:
        for name in preferred_sections:
            if name in sections and sections[name]:
                evidence_parts.append(
                    f"\n--- {name} ---\n{sections[name][:3500]}"
                )

    if evidence_parts:
        evidence = "".join(evidence_parts)
    else:
        evidence = text[:14000]

    return evidence[:18000]


def generate_research_gap(text, sections=None, client=None):
    """
    Identify potential research gaps supported by the uploaded paper.

    This does not claim to perform a complete literature review. It extracts
    evidence-based limitations, missing areas and future research directions
    from the paper itself.
    """

    if client is None:
        client = _get_client()

    if not client:
        return None

    evidence = _build_evidence(text, sections or {})

    prompt = f"""
Analyze the following research paper and identify POTENTIAL RESEARCH GAPS.

This is an evidence-based analysis of the uploaded paper, not a complete
literature review.

Very important rules:
- Do NOT invent facts, limitations, datasets, methods or missing research.
- Do NOT claim that no previous researcher has solved something unless the
  paper itself provides evidence for that claim.
- Base every identified gap on information in the supplied paper.
- If evidence for a category is insufficient, say "Not clearly identified in
  the paper" instead of guessing.
- Distinguish an author-stated limitation from a gap inferred from the paper.
- Keep the language suitable for a college research project.

Return the answer using exactly these sections:

### 1. Author-Stated Limitations
Mention limitations explicitly acknowledged by the authors.

### 2. Dataset or Data Gaps
Mention limitations involving dataset size, diversity, quality, labels,
data sources, or missing data, only when supported by the paper.

### 3. Methodology Gaps
Mention methodological limitations or areas not addressed by the proposed
approach, only when supported by the paper.

### 4. Evaluation Gaps
Mention missing experiments, metrics, comparisons, validation, generalization,
or real-world testing, only when supported by the paper.

### 5. Unexplored Areas
Identify reasonable areas that the paper leaves unexplored, and explain the
evidence from the paper.

### 6. Future Research Directions
Summarize future work explicitly mentioned by the authors and clearly label
any additional direction as a potential direction rather than established fact.

### 7. Research Gap Summary
Give a short 2-4 sentence summary of the strongest potential gaps supported by
the paper.

Research paper evidence:
{evidence}
"""

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a careful academic research assistant. "
                            "Identify potential research gaps only when supported "
                            "by the supplied research paper. Never fabricate "
                            "literature claims."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.1,
                max_completion_tokens=900,
                include_reasoning=False,
            )

            return response.choices[0].message.content

        except Exception:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
            else:
                return None

    return None
