import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


# ---------------------------------------------------------
# Get Groq API key
# Works both locally and on Streamlit Cloud
# ---------------------------------------------------------

api_key = None

try:
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")


# Create Groq client only if API key exists
client = Groq(api_key=api_key) if api_key else None


# ---------------------------------------------------------
# Abstractive Summary using Groq
# ---------------------------------------------------------

def generate_smart_summary(text):

    # If API key is missing, return None
    # so the app can use the extractive summary instead.
    if not client:
        return None

    prompt = f"""
Explain this research paper for a college student.

Include:
- What problem it solves
- Method used
- Main findings
- Why it matters

Keep the explanation clear and concise.

Maximum 180 words.

Research paper:

{text[:12000]}
"""

    # Try the API up to 3 times
    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a research paper summarization assistant. "
                            "Give accurate, simple and concise explanations."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,
                max_completion_tokens=300,

                # Avoid returning reasoning content
                include_reasoning=False
            )

            return response.choices[0].message.content

        except Exception:

            if attempt < 2:
                time.sleep(2 * (attempt + 1))

            else:
                return None

    return None