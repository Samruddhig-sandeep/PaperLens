import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

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


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="PaperLens",
    page_icon="📄",
    layout="wide"
)

load_css()

load_dotenv()


# =========================================================
# GROQ CLIENT
# =========================================================

groq_api_key = None

try:
    groq_api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    pass

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY")

groq_client = None

if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)


# =========================================================
# CACHED PAPER ANALYSIS
# =========================================================

@st.cache_data(show_spinner=False)
def analyze_paper(text):

    cleaned_text, tokens = preprocess_text(text)

    extractive_summary = generate_summary(text)

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

    return {
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "extractive_summary": extractive_summary,
        "smart_summary": smart_summary,
        "keywords": keywords,
        "domain": domain,
        "confidence": confidence,
        "sections": sections,
        "stats": stats,
        "insights": insights
    }


# =========================================================
# GROQ CHAT FUNCTION
# =========================================================

def ask_groq(messages, max_tokens=500):

    if not groq_client:
        return "Groq API key is not configured."

    try:

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.2,
            max_completion_tokens=max_tokens,
            include_reasoning=False
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Sorry, I couldn't generate a response right now.\n\nError: {str(e)}"


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero-title">📄 PaperLens</div>
    <div class="hero-subtitle">
    Research Paper Analyzer using NLP
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📄 PaperLens")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown(
        """
        - 📄 PDF Upload
        - 📝 Extractive Summary (TextRank)
        - ✨ Abstractive Summary (Groq)
        - 🔑 TF-IDF Keywords
        - 🏷️ Domain Prediction
        - 📚 Section Detection
        - 📊 Paper Statistics
        - 💡 Key Insights
        - 📑 Compare Two Papers
        - 💬 AI Paper Chatbot
        - 💾 Markdown Report
        """
    )

    st.markdown("---")

    st.caption(
        "Built with PyMuPDF, NLTK, TextRank, Groq and Scikit-learn."
    )


# =========================================================
# UPLOAD MODE
# =========================================================

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


# =========================================================
# EMPTY STATE
# =========================================================

if uploaded_file is None:

    st.markdown(
        """
        <div class="glass-card upload-card">

        # 📄 Upload a Research Paper

        Drag and drop a PDF to begin.

        PaperLens will automatically extract text, generate
        summaries, predict the research domain and create
        a downloadable report.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# SINGLE PAPER MODE
# =========================================================

if mode == "Single Paper":

    # -----------------------------------------------------
    # ANALYZE PAPER
    # -----------------------------------------------------

    with st.spinner("Analyzing research paper..."):

        text = extract_text_from_pdf(uploaded_file)

        metadata = extract_paper_metadata(uploaded_file)

        analysis = analyze_paper(text)

    cleaned_text = analysis["cleaned_text"]
    tokens = analysis["tokens"]
    extractive_summary = analysis["extractive_summary"]
    smart_summary = analysis["smart_summary"]
    keywords = analysis["keywords"]
    domain = analysis["domain"]
    confidence = analysis["confidence"]
    sections = analysis["sections"]
    stats = analysis["stats"]
    insights = analysis["insights"]


    # -----------------------------------------------------
    # PAPER PROFILE
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="glass-card">

        # {metadata["title"]}

        **👤 Authors:** {metadata["authors"]}

        **📅 Year:** {metadata["year"]}

        <div style="margin-top:15px;">

        <span class="chip blue">{domain}</span>

        <span class="chip purple">
        {confidence}% confidence
        </span>

        <span class="chip pink">
        {stats["Reading Time"]} min read
        </span>

        <span class="chip green">
        {stats["Words"]} words
        </span>

        </div>

        <hr>

        ### Abstract Preview

        {metadata["abstract"][:500]}...

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    overview, summary_tab, chat_tab, keyword_tab, section_tab, insight_tab = st.tabs(
        [
            "📊 Overview",
            "📝 Summary",
            "💬 Ask PaperLens",
            "🔑 Keywords",
            "📚 Sections",
            "💡 Insights"
        ]
    )


    # =====================================================
    # OVERVIEW
    # =====================================================

    with overview:

        st.subheader("Document Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Words",
                stats["Words"]
            )

            st.metric(
                "Characters",
                stats["Characters"]
            )

        with c2:

            st.metric(
                "Unique Words",
                stats["Unique Words"]
            )

            st.metric(
                "Sentences",
                stats["Sentences"]
            )

        with c3:

            st.metric(
                "Reading Time",
                f'{stats["Reading Time"]} min'
            )

            st.metric(
                "Avg Sentence Length",
                stats["Avg Sentence Length"]
            )

        st.divider()

        st.subheader("Extracted Text")

        st.text_area(
            "Extracted Text",
            text[:3000],
            height=300,
            label_visibility="collapsed"
        )


    # =====================================================
    # SUMMARY
    # =====================================================

    with summary_tab:

        left, right = st.columns(2)

        with left:

            st.markdown(
                """
                <div class="glass-card">

                ## 📝 Extractive Summary

                **Classical NLP — TextRank**

                Selects the most important sentences
                directly from the original paper.

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(extractive_summary)

            st.code(
                extractive_summary,
                language="text"
            )


        with right:

            st.markdown(
                """
                <div class="glass-card">

                ## ✨ Abstractive Summary

                **LLM-based — Groq**

                Rewrites the paper into simpler language
                while preserving the main ideas.

                </div>
                """,
                unsafe_allow_html=True
            )

            if smart_summary:

                st.write(smart_summary)

                st.code(
                    smart_summary,
                    language="text"
                )

            else:

                st.warning(
                    "Groq summary is temporarily unavailable. "
                    "The Extractive Summary is still available."
                )


    # =====================================================
    # SINGLE PAPER CHATBOT
    # =====================================================

    with chat_tab:

        st.subheader("💬 Ask PaperLens")

        st.caption(
            "Ask questions about this research paper."
        )

        # -------------------------------------------------
        # SESSION STATE
        # -------------------------------------------------

        if "single_chat_history" not in st.session_state:

            st.session_state.single_chat_history = []


        # -------------------------------------------------
        # CLEAR CHAT
        # -------------------------------------------------

        if st.button(
            "🗑️ Clear Chat",
            key="clear_single_chat"
        ):

            st.session_state.single_chat_history = []

            st.rerun()


        # -------------------------------------------------
        # CHATBOT
        # -------------------------------------------------

        @st.fragment
        def single_paper_chatbot():

            # ---------------------------------------------
            # PAPER CONTEXT
            # ---------------------------------------------

            paper_context = f"""
Research Paper Information

Title:
{metadata["title"]}

Authors:
{metadata["authors"]}

Year:
{metadata["year"]}

Domain:
{domain}

Abstract:
{metadata["abstract"][:3000]}

Extractive Summary:
{extractive_summary[:4000]}

Abstractive Summary:
{smart_summary[:4000] if smart_summary else "Not available"}

Keywords:
{", ".join([k for k, _ in keywords[:10]])}

Paper Text:
{text[:10000]}
"""


            # ---------------------------------------------
            # DISPLAY CHAT HISTORY
            # ---------------------------------------------

            for message in st.session_state.single_chat_history:

                with st.chat_message(message["role"]):

                    st.write(message["content"])


            # ---------------------------------------------
            # SUGGESTED QUESTIONS
            # ---------------------------------------------

            st.markdown("#### Suggested Questions")

            q1, q2, q3 = st.columns(3)

            with q1:

                if st.button(
                    "What is this paper about?",
                    key="single_q1"
                ):

                    st.session_state.single_question = (
                        "What is this paper about?"
                    )

                    st.rerun(scope="fragment")


            with q2:

                if st.button(
                    "What methodology was used?",
                    key="single_q2"
                ):

                    st.session_state.single_question = (
                        "What methodology was used in this paper?"
                    )

                    st.rerun(scope="fragment")


            with q3:

                if st.button(
                    "What are the main findings?",
                    key="single_q3"
                ):

                    st.session_state.single_question = (
                        "What are the main findings of this paper?"
                    )

                    st.rerun(scope="fragment")


            # ---------------------------------------------
            # USER INPUT
            # ---------------------------------------------

            question = st.chat_input(
                "Ask something about this paper..."
            )


            # Suggested question handling

            if "single_question" in st.session_state:

                question = st.session_state.single_question

                del st.session_state.single_question


            # ---------------------------------------------
            # PROCESS QUESTION
            # ---------------------------------------------

            if question:

                st.session_state.single_chat_history.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                with st.chat_message("user"):

                    st.write(question)


                # Keep only recent conversation
                recent_history = (
                    st.session_state.single_chat_history[-6:]
                )


                messages = [
                    {
                        "role": "system",
                        "content": """
You are PaperLens, an AI assistant for research papers.

Answer questions using the supplied paper context.

Rules:
- Stay focused on the research paper.
- Do not invent information.
- If the answer is not available in the paper, say so.
- Explain technical concepts in simple language.
- Keep answers concise but useful.
- Use the paper's terminology when appropriate.
"""
                    },
                    {
                        "role": "user",
                        "content": paper_context
                    }
                ]


                for message in recent_history:

                    messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    )


                with st.chat_message("assistant"):

                    with st.spinner("Thinking..."):

                        answer = ask_groq(
                            messages,
                            max_tokens=500
                        )

                    st.write(answer)


                st.session_state.single_chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


        single_paper_chatbot()


    # =====================================================
    # KEYWORDS
    # =====================================================

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

            chips += (
                f'<span class="chip '
                f'{colors[i % 5]}">{keyword}</span> '
            )

        st.markdown(
            chips,
            unsafe_allow_html=True
        )

        st.divider()

        st.subheader("Keyword Importance")

        for keyword, score in keywords:

            st.progress(
                min(score * 5, 1),
                text=f"{keyword} ({score:.3f})"
            )


    # =====================================================
    # SECTIONS
    # =====================================================

    with section_tab:

        if sections:

            for title, content in sections.items():

                with st.expander(
                    f"📄 {title}"
                ):

                    st.write(
                        content[:4000]
                    )

        else:

            st.warning(
                "No standard sections detected."
            )


    # =====================================================
    # INSIGHTS
    # =====================================================

    with insight_tab:

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
                <div class="glass-card">

                ### Research Domain

                {domain}

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="glass-card">

                ### Years Mentioned

                {", ".join(insights["Years Mentioned"])}

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                """
                <div class="glass-card">

                ### Top Keywords

                {}

                </div>
                """.format(
                    "<br>".join(
                        insights["Top Keywords"]
                    )
                ),
                unsafe_allow_html=True
            )

        st.subheader("Key Findings")

        for finding in insights["Key Findings"]:

            st.markdown(
                f"""
                <div class="glass-card">
                💡 {finding}
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

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

{smart_summary if smart_summary else "Groq summary unavailable."}

---

## Keywords
"""

    for keyword, score in keywords:

        report += (
            f"- {keyword} ({score:.3f})\n"
        )

    report += "\n## Key Findings\n"

    for finding in insights["Key Findings"]:

        report += (
            f"- {finding}\n"
        )

    st.download_button(
        "📥 Download Report",
        report,
        file_name="paperlens_report.md",
        mime="text/markdown"
    )


# =========================================================
# COMPARE TWO PAPERS
# =========================================================

else:

    if uploaded_file and second_file:

        st.title(
            "📑 Compare Two Research Papers"
        )


        # -------------------------------------------------
        # PROCESS FUNCTION
        # -------------------------------------------------

        def process(file):

            text = extract_text_from_pdf(file)

            meta = extract_paper_metadata(file)

            analysis = analyze_paper(text)

            return {
                "meta": meta,
                "domain": analysis["domain"],
                "confidence": analysis["confidence"],
                "extractive": analysis["extractive_summary"],
                "abstractive": analysis["smart_summary"],
                "keywords": analysis["keywords"],
                "stats": analysis["stats"],
                "text": text
            }


        # -------------------------------------------------
        # ANALYZE BOTH PAPERS
        # -------------------------------------------------

        with st.spinner(
            "Analyzing both research papers..."
        ):

            paper1 = process(uploaded_file)

            paper2 = process(second_file)


            # -------------------------------------------------
            # COMPARISON
            # -------------------------------------------------

            result = compare_papers(
                paper1["meta"],
                paper2["meta"],

                paper1["domain"],
                paper2["domain"],

                paper1["extractive"],
                paper2["extractive"],

                paper1["abstractive"],
                paper2["abstractive"],

                paper1["keywords"],
                paper2["keywords"],

                paper1["stats"],
                paper2["stats"]
            )


        # -------------------------------------------------
        # PAPER CARDS
        # -------------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
                <div class="glass-card">

                ## 📘 Paper A

                **{result["Paper A"]["Title"]}**

                📅 {result["Paper A"]["Year"]}

                🏷️ {result["Paper A"]["Domain"]}

                📖 {result["Paper A"]["Reading Time"]} min

                🔑 {result["Paper A"]["Keywords"]}

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "### 📝 Extractive Summary (TextRank)"
            )

            st.write(
                result["Paper A"]["Extractive"]
            )

            st.markdown(
                "### ✨ Abstractive Summary (Groq)"
            )

            if result["Paper A"]["Abstractive"]:

                st.write(
                    result["Paper A"]["Abstractive"]
                )

            else:

                st.info(
                    "Groq summary unavailable. "
                    "Showing the extractive summary instead."
                )


        with c2:

            st.markdown(
                f"""
                <div class="glass-card">

                ## 📙 Paper B

                **{result["Paper B"]["Title"]}**

                📅 {result["Paper B"]["Year"]}

                🏷️ {result["Paper B"]["Domain"]}

                📖 {result["Paper B"]["Reading Time"]} min

                🔑 {result["Paper B"]["Keywords"]}

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "### 📝 Extractive Summary (TextRank)"
            )

            st.write(
                result["Paper B"]["Extractive"]
            )

            st.markdown(
                "### ✨ Abstractive Summary (Groq)"
            )

            if result["Paper B"]["Abstractive"]:

                st.write(
                    result["Paper B"]["Abstractive"]
                )

            else:

                st.info(
                    "Groq summary unavailable. "
                    "Showing the extractive summary instead."
                )


        # -------------------------------------------------
        # QUICK COMPARISON
        # -------------------------------------------------

        st.markdown("---")

        st.subheader(
            "📊 Quick Comparison"
        )

        st.table(
            {
                "Feature": [
                    "Domain",
                    "Year",
                    "Words",
                    "Reading Time"
                ],

                "Paper A": [
                    str(
                        result["Paper A"]["Domain"]
                    ),

                    str(
                        result["Paper A"]["Year"]
                    ),

                    str(
                        result["Paper A"]["Words"]
                    ),

                    str(
                        result["Paper A"]["Reading Time"]
                    )
                ],

                "Paper B": [
                    str(
                        result["Paper B"]["Domain"]
                    ),

                    str(
                        result["Paper B"]["Year"]
                    ),

                    str(
                        result["Paper B"]["Words"]
                    ),

                    str(
                        result["Paper B"]["Reading Time"]
                    )
                ]
            }
        )


        # =================================================
        # COMPARE CHATBOT
        # =================================================

        st.markdown("---")

        st.subheader(
            "💬 Ask About Both Papers"
        )

        st.caption(
            "Ask PaperLens to explain similarities, differences "
            "or specific details from either paper."
        )


        # -------------------------------------------------
        # SESSION STATE
        # -------------------------------------------------

        if "compare_chat_history" not in st.session_state:

            st.session_state.compare_chat_history = []


        # -------------------------------------------------
        # CLEAR CHAT
        # -------------------------------------------------

        if st.button(
            "🗑️ Clear Comparison Chat",
            key="clear_compare_chat"
        ):

            st.session_state.compare_chat_history = []

            st.rerun()


        # -------------------------------------------------
        # COMPARE CHATBOT
        # -------------------------------------------------

        @st.fragment
        def comparison_chatbot():

            # ---------------------------------------------
            # CONTEXT
            # ---------------------------------------------

            paper_a_context = f"""
PAPER A

Title:
{paper1["meta"]["title"]}

Authors:
{paper1["meta"]["authors"]}

Year:
{paper1["meta"]["year"]}

Domain:
{paper1["domain"]}

Abstract:
{paper1["meta"]["abstract"][:2500]}

Extractive Summary:
{paper1["extractive"][:3500]}

Abstractive Summary:
{
    paper1["abstractive"][:3500]
    if paper1["abstractive"]
    else "Not available"
}

Keywords:
{", ".join([k for k, _ in paper1["keywords"][:10]])}

Paper Text:
{paper1["text"][:8000]}
"""


            paper_b_context = f"""
PAPER B

Title:
{paper2["meta"]["title"]}

Authors:
{paper2["meta"]["authors"]}

Year:
{paper2["meta"]["year"]}

Domain:
{paper2["domain"]}

Abstract:
{paper2["meta"]["abstract"][:2500]}

Extractive Summary:
{paper2["extractive"][:3500]}

Abstractive Summary:
{
    paper2["abstractive"][:3500]
    if paper2["abstractive"]
    else "Not available"
}

Keywords:
{", ".join([k for k, _ in paper2["keywords"][:10]])}

Paper Text:
{paper2["text"][:8000]}
"""


            comparison_context = (
                paper_a_context
                + "\n\n"
                + paper_b_context
            )


            # ---------------------------------------------
            # DISPLAY HISTORY
            # ---------------------------------------------

            for message in (
                st.session_state.compare_chat_history
            ):

                with st.chat_message(
                    message["role"]
                ):

                    st.write(
                        message["content"]
                    )


            # ---------------------------------------------
            # SUGGESTED QUESTIONS
            # ---------------------------------------------

            st.markdown(
                "#### Suggested Questions"
            )

            q1, q2, q3 = st.columns(3)

            with q1:

                if st.button(
                    "What is common?",
                    key="compare_q1"
                ):

                    st.session_state.compare_question = (
                        "What are the main similarities between "
                        "the two papers?"
                    )

                    st.rerun(scope="fragment")


            with q2:

                if st.button(
                    "How are methods different?",
                    key="compare_q2"
                ):

                    st.session_state.compare_question = (
                        "How do the methodologies of the two "
                        "papers differ?"
                    )

                    st.rerun(scope="fragment")


            with q3:

                if st.button(
                    "Compare the findings",
                    key="compare_q3"
                ):

                    st.session_state.compare_question = (
                        "Compare the main findings of the two papers."
                    )

                    st.rerun(scope="fragment")


            # ---------------------------------------------
            # INPUT
            # ---------------------------------------------

            question = st.chat_input(
                "Ask about either paper..."
            )


            if "compare_question" in st.session_state:

                question = (
                    st.session_state.compare_question
                )

                del st.session_state.compare_question


            # ---------------------------------------------
            # PROCESS
            # ---------------------------------------------

            if question:

                st.session_state.compare_chat_history.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                with st.chat_message("user"):

                    st.write(question)


                recent_history = (
                    st.session_state.compare_chat_history[-6:]
                )


                messages = [
                    {
                        "role": "system",
                        "content": """
You are PaperLens, an AI assistant that compares research papers.

Answer using only the supplied paper context.

Rules:
- Clearly distinguish Paper A and Paper B.
- Explain similarities and differences.
- Do not invent information.
- If something is not available in the papers, say so.
- Do not assume one paper is better.
- Do not create rankings or scores.
- Keep answers clear and concise.
"""
                    },

                    {
                        "role": "user",
                        "content": comparison_context
                    }
                ]


                for message in recent_history:

                    messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    )


                with st.chat_message("assistant"):

                    with st.spinner("Comparing papers..."):

                        answer = ask_groq(
                            messages,
                            max_tokens=600
                        )

                    st.write(answer)


                st.session_state.compare_chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


        comparison_chatbot()


    else:

        st.info(
            "Upload both Paper A and Paper B to compare them."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        padding:25px;
    ">
    PaperLens • Research Paper Analyzer using NLP
    </div>
    """,
    unsafe_allow_html=True
)