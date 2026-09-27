
import streamlit as st
from pdf_reader import extract_text_from_pdf, extract_paper_metadata
from preprocess import preprocess_text
from keyword_extractor import extract_keywords
from summarizer import generate_summary
from smart_summary import generate_smart_summary
from domain_classifier import predict_domain
from section_splitter import split_sections
from paper_stats import get_stats
from insights_generator import generate_insights
from comparison import compare_papers
from styles import load_css

# ---------------------------------------------------
# Page Setup
# ---------------------------------------------------

st.set_page_config(
    page_title="PaperLens",
    page_icon="📄",
    layout="wide"
)

load_css()

# ---------------------------------------------------
# Hero
# ---------------------------------------------------

st.markdown("""
<div class="hero-title">📄 PaperLens</div>
<div class="hero-subtitle">
Research Paper Analyzer using NLP
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("📄 PaperLens")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
- 📄 PDF Upload
- 📝 Extractive Summary (TextRank)
- ✨ Abstractive Summary (Gemini)
- 🔑 TF-IDF Keywords
- 🏷️ Domain Prediction
- 📚 Section Detection
- 📊 Paper Statistics
- 💡 Key Insights
- 📑 Compare Two Papers
- 💾 Markdown Report
""")

    st.markdown("---")

    st.caption("Built with PyMuPDF, NLTK, TextRank, Gemini and Scikit-learn.")

# ---------------------------------------------------
# Upload Mode
# ---------------------------------------------------

mode = st.radio(
    "Choose Mode",
    ["Single Paper", "Compare Two Papers"],
    horizontal=True
)

second_file = None

if mode == "Single Paper":

    uploaded_file = st.file_uploader(
        "Upload Research Paper",
        type=["pdf"]
    )

else:

    c1, c2 = st.columns(2)

    with c1:
        uploaded_file = st.file_uploader(
            "Paper A",
            type=["pdf"],
            key="paperA"
        )

    with c2:
        second_file = st.file_uploader(
            "Paper B",
            type=["pdf"],
            key="paperB"
        )

# ---------------------------------------------------
# Empty State
# ---------------------------------------------------

if uploaded_file is None:

    st.markdown("""
<div class="glass-card upload-card">

# 📄 Upload a Research Paper

Drag and drop a PDF to begin.

PaperLens will automatically extract text, generate summaries,
predict the research domain and create a downloadable report.

</div>
""", unsafe_allow_html=True)

    st.stop()

# ---------------------------------------------------
# SINGLE PAPER MODE
# ---------------------------------------------------

if mode == "Single Paper":

    with st.spinner("Analyzing research paper..."):

        text = extract_text_from_pdf(uploaded_file)

        metadata = extract_paper_metadata(uploaded_file)

        cleaned_text, tokens = preprocess_text(text)

        # Always works (offline NLP)
        extractive_summary = generate_summary(text)

        # Returns None if Gemini fails
        smart_summary = generate_smart_summary(text)

        keywords = extract_keywords(cleaned_text)

        domain, confidence = predict_domain(cleaned_text)

        sections = split_sections(text)

        stats = get_stats(text, tokens)

        insights = generate_insights(
            text,
            extractive_summary,
            keywords
        )

    # ------------------------------------------------
    # Paper Profile Card
    # ------------------------------------------------

    st.markdown(f"""
<div class="glass-card">

# {metadata["title"]}

**👤 Authors:** {metadata["authors"]}

**📅 Year:** {metadata["year"]}

<div style="margin-top:15px;">

<span class="chip blue">{domain}</span>

<span class="chip purple">{confidence}% confidence</span>

<span class="chip pink">{stats["Reading Time"]} min read</span>

<span class="chip green">{stats["Words"]} words</span>

</div>

<hr>

### Abstract Preview

{metadata["abstract"][:500]}...

</div>
""", unsafe_allow_html=True)

    # ------------------------------------------------
    # Tabs
    # ------------------------------------------------

    overview, summary_tab, keyword_tab, section_tab, insight_tab = st.tabs([
        "📊 Overview",
        "📝 Summary",
        "🔑 Keywords",
        "📚 Sections",
        "💡 Insights"
    ])

    # =================================================
    # OVERVIEW
    # =================================================

    with overview:

        st.subheader("Document Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Words", stats["Words"])
            st.metric("Characters", stats["Characters"])

        with c2:
            st.metric("Unique Words", stats["Unique Words"])
            st.metric("Sentences", stats["Sentences"])

        with c3:
            st.metric("Reading Time", f'{stats["Reading Time"]} min')
            st.metric("Avg Sentence Length", stats["Avg Sentence Length"])

        st.divider()

        st.subheader("Extracted Text")

        st.text_area(
            "",
            text[:3000],
            height=300
        )

    # =================================================
    # SUMMARY
    # =================================================

    with summary_tab:

        left, right = st.columns(2)

        with left:

            st.markdown("""
<div class="glass-card">

## 📝 Extractive Summary (TextRank)

**Classical NLP**

Selects the most important sentences directly from the original paper.

</div>
""", unsafe_allow_html=True)

            st.write(extractive_summary)

            st.code(extractive_summary, language="text")

        with right:

            st.markdown("""
<div class="glass-card">

## ✨ Abstractive Summary (Gemini)

**LLM-based**

Rewrites the paper into simpler language.

</div>
""", unsafe_allow_html=True)

            if smart_summary:

                st.write(smart_summary)

                st.code(smart_summary, language="text")

            else:

                st.warning(
                    "⚠️ Gemini is experiencing high demand right now. "
                    "The Extractive Summary is still available."
                )

    # =================================================
    # KEYWORDS
    # =================================================

    with keyword_tab:

        st.subheader("Top Keywords")

        colors = [
            "blue",
            "purple",
            "pink",
            "green",
            "orange"
        ]

        chips = ""

        for i, (keyword, score) in enumerate(keywords):

            chips += f'<span class="chip {colors[i%5]}">{keyword}</span> '

        st.markdown(chips, unsafe_allow_html=True)

        st.divider()

        st.subheader("Keyword Importance")

        for keyword, score in keywords:

            st.progress(
                min(score * 5, 1),
                text=f"{keyword} ({score:.3f})"
            )

    # =================================================
    # SECTIONS
    # =================================================

    with section_tab:

        if sections:

            for title, content in sections.items():

                with st.expander(f"📄 {title}"):

                    st.write(content[:4000])

        else:

            st.warning("No standard sections detected.")

    # =================================================
    # INSIGHTS
    # =================================================

    with insight_tab:

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(f"""
<div class="glass-card">

### Research Domain

{domain}

</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="glass-card">

### Years Mentioned

{", ".join(insights["Years Mentioned"])}

</div>
""", unsafe_allow_html=True)

        with c2:

            st.markdown("""
<div class="glass-card">

### Top Keywords

{}

</div>
""".format("<br>".join(insights["Top Keywords"])), unsafe_allow_html=True)

        st.subheader("Key Findings")

        for finding in insights["Key Findings"]:

            st.markdown(f"""
<div class="glass-card">
💡 {finding}
</div>
""", unsafe_allow_html=True)

    # =================================================
    # DOWNLOAD REPORT
    # =================================================

    report = f"""# PaperLens Report

## {metadata["title"]}

**Authors:** {metadata["authors"]}

**Year:** {metadata["year"]}

**Domain:** {domain} ({confidence}% confidence)

---

## Extractive Summary

{extractive_summary}

---

## Abstractive Summary

{smart_summary if smart_summary else "Gemini summary unavailable due to temporary server load."}

---

## Keywords
"""

    for keyword, score in keywords:
        report += f"- {keyword} ({score:.3f})\n"

    report += "\n## Key Findings\n"

    for finding in insights["Key Findings"]:
        report += f"- {finding}\n"

    st.download_button(
        "📥 Download Report",
        report,
        file_name="paperlens_report.md",
        mime="text/markdown"
    )

# ---------------------------------------------------
# COMPARE TWO PAPERS
# ---------------------------------------------------

else:

    if uploaded_file and second_file:

        st.title("📑 Compare Two Research Papers")

        def process(file):

            text = extract_text_from_pdf(file)

            meta = extract_paper_metadata(file)

            clean, tok = preprocess_text(text)

            domain, conf = predict_domain(clean)

            summary = generate_summary(text)

            keywords = extract_keywords(clean)

            stats = get_stats(text, tok)

            return {
                "meta": meta,
                "domain": domain,
                "confidence": conf,
                "summary": summary,
                "keywords": keywords,
                "stats": stats
            }

        with st.spinner("Comparing papers..."):

            paper1 = process(uploaded_file)

            paper2 = process(second_file)

            compare_papers(
                paper1["meta"],
                paper2["meta"],
                paper1["domain"],
                paper2["domain"],
                paper1["summary"],
                paper2["summary"],
                paper1["keywords"],
                paper2["keywords"],
                paper1["stats"],
                paper2["stats"]
            )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(f"""
<div class="glass-card">

## 📘 Paper A

**{paper1["meta"]["title"]}**

📅 {paper1["meta"]["year"]}

🏷️ {paper1["domain"]}

📖 {paper1["stats"]["Reading Time"]} min

🔑 {", ".join([k for k,_ in paper1["keywords"][:5]])}

</div>
""", unsafe_allow_html=True)

            st.write(paper1["summary"])

        with c2:

            st.markdown(f"""
<div class="glass-card">

## 📙 Paper B

**{paper2["meta"]["title"]}**

📅 {paper2["meta"]["year"]}

🏷️ {paper2["domain"]}

📖 {paper2["stats"]["Reading Time"]} min

🔑 {", ".join([k for k,_ in paper2["keywords"][:5]])}

</div>
""", unsafe_allow_html=True)

            st.write(paper2["summary"])

        st.subheader("Quick Comparison")

        st.table({
            "Feature": [
                "Domain",
                "Year",
                "Words",
                "Reading Time"
            ],
            "Paper A": [
                paper1["domain"],
                paper1["meta"]["year"],
                paper1["stats"]["Words"],
                paper1["stats"]["Reading Time"]
            ],
            "Paper B": [
                paper2["domain"],
                paper2["meta"]["year"],
                paper2["stats"]["Words"],
                paper2["stats"]["Reading Time"]
            ]
        })

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("""
<div style="text-align:center;color:#64748B;padding:25px;">
PaperLens • Research Paper Analyzer using NLP
</div>
""", unsafe_allow_html=True)