# AI Resume Screening System

An end-to-end AI-powered recruitment tool that ranks candidates against a job description using semantic similarity and skill matching.

## What it does

- Upload a job description and multiple PDF resumes
- Extracts skills from both using the ESCO skills taxonomy
- Computes semantic similarity using Sentence Transformers
- Combines both signals into a final candidate score
- Displays ranked results in a clean Streamlit dashboard

## How it works

```
JD + Resumes
     ↓
Text Cleaning (preprocess.py)
     ↓
Skill Extraction via ESCO (skill_extractor.py)
     ↓
Semantic Matching via Sentence Transformers (matcher.py)
     ↓
Skill Overlap Scoring (scorer.py)
     ↓
Final Score = 70% Semantic + 30% Skill Match
     ↓
Streamlit Dashboard
```

## Tech Stack

- **Sentence Transformers** — `all-MiniLM-L6-v2` for semantic embeddings
- **ESCO Skills Taxonomy** — 13,000+ professional skills with aliases
- **Streamlit** — interactive web dashboard
- **pdfplumber / PyMuPDF** — PDF text extraction
- **pandas** — data processing

## Project Structure

```
AI-Recruitment-Assistant/
├── data/
│   ├── resumes/         # Resume.csv
│   ├── jobs/            # monster_com-job_sample.csv
│   └── skills/          # skills_en.csv (ESCO)
├── src/
│   ├── preprocess.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   ├── scorer.py
│   ├── ranker.py
│   ├── pipeline.py
│   ├── pdf_parser.py
│   └── phrase_extractor.py
├── app/
│   └── streamlit_app.py
├── main.py
└── requirements.txt
```

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/yourusername/AI-Recruitment-Assistant.git
   cd AI-Recruitment-Assistant
   ```

2. Install dependencies
   ```bash
   uv add pandas numpy scikit-learn sentence-transformers pdfplumber streamlit spacy python-dotenv google-generativeai
   ```

3. Download datasets
   - [Resume Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset) → `data/resumes/Resume.csv`
   - [Monster Jobs](https://www.kaggle.com/datasets/PromptCloudHQ/us-jobs-on-monstercom) → `data/jobs/monster_com-job_sample.csv`
   - [ESCO Skills](https://esco.ec.europa.eu/en/use-esco/download) → `data/skills/skills_en.csv`

4. Add your Gemini API key — create a `.env` file in the root of the project:
   ```
   GEMINI_API_KEY=your_key_here
   ```

5. Run the app
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Usage

1. Paste a job description into the text area
2. Upload one or more PDF resumes
3. Click **Analyze Resumes**
4. View ranked candidates with scores, skill gaps, and AI summaries

## Scoring

| Signal | Weight |
|---|---|
| Semantic Similarity | 70% |
| Skill Match | 30% |

## Notes

- Rename resume PDFs to candidate names before uploading (e.g. `john_doe.pdf`)
- Gemini summaries require a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Free Gemini tier allows 1,500 requests/day
- Never commit your `.env` file — make sure it is listed in `.gitignore`
