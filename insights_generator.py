
import re

def generate_insights(text, summary, keywords):

    years = sorted(set(re.findall(r"\b(?:19|20)\d{2}\b", text)))

    findings = []

    lower_text = text.lower()
    lower_summary = summary.lower()

    if "outperform" in lower_summary:
        findings.append("The paper compares multiple methods and reports performance differences.")

    if "dataset" in lower_text:
        findings.append("The study evaluates one or more datasets.")

    if "camera trap" in lower_text:
        findings.append("The research focuses on camera-trap imagery.")

    if "vision-language" in lower_text or "vlm" in lower_text:
        findings.append("The paper investigates Vision-Language Models.")

    if "edge" in lower_text:
        findings.append("The research emphasizes edge-device deployment.")

    if not findings:
        findings.append("Important findings were extracted from the paper.")

    return {
        "Top Keywords":[k for k,_ in keywords[:5]],
        "Years Mentioned": years if years else ["None"],
        "Key Findings": findings
    }