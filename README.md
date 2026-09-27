
# 📄 PaperLens

### Research Paper Analyzer using NLP

PaperLens is an NLP-powered web application that helps students and researchers understand academic papers faster. Users can upload a PDF research paper and automatically extract summaries, keywords, research domains, sections, and key insights through a modern interactive dashboard.

> Built using **Python, Streamlit, NLTK, TF-IDF, TextRank, Naive Bayes, and Gemini**.

---


## Features

- 📄 Upload research papers in PDF format
- 📝 **Extractive Summary** using TextRank
- ✨ **Abstractive Summary** using Gemini
- 🔑 TF-IDF Keyword Extraction
- 🏷️ Research Domain Prediction with Confidence
- 📚 Automatic Section Detection
- 📊 Paper Statistics
- 💡 Key Insights
- 📑 Compare Two Research Papers
- 💾 Download analysis as Markdown

---

## How It Works

1. Upload a research paper.
2. PaperLens extracts text using PyMuPDF.
3. The text is preprocessed using NLTK.
4. TextRank generates an extractive summary.
5. Gemini creates an abstractive summary.
6. TF-IDF extracts important keywords.
7. Naive Bayes predicts the research domain.
8. The app displays sections, insights, and statistics.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web App |
| PyMuPDF | PDF Text Extraction |
| NLTK | Text Preprocessing |
| Scikit-learn | TF-IDF & Naive Bayes |
| Sumy | TextRank Summarization |
| Gemini | Abstractive Summarization |

---

## Project Structure

```text
PaperLens/
├── app.py
├── styles.py
├── smart_summary.py
├── pdf_reader.py
├── preprocess.py
├── keyword_extractor.py
├── summarizer.py
├── domain_classifier.py
├── section_splitter.py
├── paper_stats.py
├── insights_generator.py
├── comparison.py
├── training_data.csv
├── requirements.txt
└── README.md
```

## Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/PaperLens.git
cd PaperLens
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```text
GEMINI_API_KEY=Your_API_Key
```

Run the application.

```bash
streamlit run app.py
```

---

## Future Enhancements

- Literature Review Matrix
- Citation Extraction
- Reference Detection
- Multi-paper comparison
- PDF Report Export
- Dark/Light Theme Toggle

---

## Author

**Samruddhi Gopalkar**

Computer Engineering Student | NLP Mini Project