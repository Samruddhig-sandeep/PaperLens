import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_smart_summary(text):
    prompt = f"""
Explain this research paper for a college student.

Include:
- What problem it solves
- Method used
- Main findings
- Why it matters

Maximum 180 words.

{text[:12000]}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            return response.text

        except Exception:
            if attempt < 2:
                time.sleep(2)
            else:
                return None