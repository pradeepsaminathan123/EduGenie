# EduGenie: Google Gemini Powered Learning Assistant 🎓

EduGenie is a full-stack AI-powered educational web application designed to empower students and lifelong learners with instant Q&A, simple concept explanations, text summarization, auto-generated interactive quizzes, and structured learning roadmaps.

---

## 🚀 Features

1. **Ask EduGenie a Question (`/qa`)**:
   - High-precision Q&A engine powered by **Google Gemini 1.5 Pro**.
   - Answers student queries with step-by-step clarity.

2. **Need an Explanation? (`/explain/`)**:
   - School-student friendly, simple explanations powered by the local **`MBZUAI/LaMini-Flan-T5-783M`** Hugging Face model.
   - Runs locally without external API dependencies.

3. **Summarize a Paragraph (`/summarize/`)**:
   - Condenses lengthy passages or textbook excerpts into essential takeaways using **Google Gemini 1.5 Pro**.

4. **Generate Interactive Quizzes (`/quiz`)**:
   - Automatically generates exactly 3 high-quality multiple choice questions (MCQs) with 4 options from any study material.
   - Dynamic frontend with instant validation (green for correct, red with answer revealed for incorrect).

5. **Get Learning Recommendations (`/learn/recommendations`)**:
   - Generates a personalized curriculum with Beginner (1-2 weeks), Intermediate (2-3 weeks), and Advanced (3-4+ weeks) breakdowns, along with tutorials, books, and practice platforms.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.10+, FastAPI, Uvicorn, Jinja2, Pydantic, python-dotenv
- **AI / ML Models:**
  - **Local:** `MBZUAI/LaMini-Flan-T5-783M` via Hugging Face `transformers` & `torch`
  - **Cloud:** Google Gemini (`gemini-1.5-pro`) via `google-generativeai` SDK
- **Frontend:** HTML5, Modern CSS3 (Responsive Card UI), Vanilla JavaScript (Async Fetch API)

---

## 📁 Project Structure

```text
EduGenie/
├── explanation_module.py  # Local Hugging Face LaMini-Flan-T5 explanation pipeline
├── qna.py                 # Gemini 1.5 Pro Q&A pipeline
├── quiz_module.py         # Gemini 1.5 Pro MCQ generation & JSON parser
├── summary_module.py      # Gemini 1.5 Pro paragraph summarizer
├── learning_path.py       # Gemini 1.5 Pro structured learning roadmap engine
├── main.py                # FastAPI server, endpoints, and static/template routing
├── requirements.txt       # Python dependencies
├── .env.example           # API key configuration template
├── README.md              # Documentation and guide
├── templates/
│   └── index.html         # Responsive, card-based web UI
└── static/
    ├── style.css          # Modern typography, colors, responsive layouts, badges
    └── script.js          # Async fetch callers, dynamic quiz rendering, validation
```

---

## ⚡ Quickstart Guide

### 1. Clone or Open the Project
Open terminal / command prompt in the `EduGenie` folder:
```powershell
cd C:\Users\logap\Desktop\EduGenie
```

### 2. Create and Activate a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key
Create a `.env` file in the `EduGenie` root folder (or copy `.env.example`):
```powershell
copy .env.example .env
```
Open `.env` and add your Google Gemini API Key:
```env
GOOGLE_API_KEY=AIzaSy...
```
*(Get your free API key at [Google AI Studio](https://aistudio.google.com/app/apikey))*

### 5. Run the Application
```powershell
python main.py
```
Or with Uvicorn directly:
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Open in Browser
Navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 API Endpoints Reference

| Method | Endpoint | Description | Request / Query | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Web UI | None | HTML page |
| `GET` | `/qa?question=...` | Gemini Q&A | Query `question` | `{"answer": "..."}` |
| `POST` | `/explain/` | Local LaMini Explanation | `{"topic": "..."}` | `{"topic": "...", "explanation": "..."}` |
| `POST` | `/summarize/` | Paragraph Summary | `{"text": "..."}` | `{"summary": "..."}` |
| `POST` | `/quiz` | 3 MCQ Quiz Generator | `{"text": "..."}` | `{"quiz": [{"question": "...", "options": [...], "answer": "..."}]}` |
| `GET` | `/learn/recommendations?topic=...` | Learning Roadmap | Query `topic` | `{"topic": "...", "recommendation": "..."}` |

---

## 📜 License
MIT License. Created with ❤️ for EduGenie.
