import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Load environment variables
load_dotenv()

# Import core AI modules
from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie: Google Gemini Powered Learning Assistant",
    description="Full-stack AI-powered educational web app with Q&A, local ML explanations, summarization, quiz generation, and personalized learning paths.",
    version="1.0.0"
)

# Mount static directory for CSS/JS
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup Jinja2 templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)


# -------------------------------------------------------------
# Pydantic Request Models
# -------------------------------------------------------------
class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Topic to explain")

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text paragraph to summarize")

class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text passage or subject for quiz generation")


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Renders the main EduGenie user interface."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/qa")
async def get_qna_answer(question: str = Query(..., min_length=1, description="The student's question")):
    """
    Answers a question using Google Gemini 1.5 Pro.
    """
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question parameter cannot be empty.")
    try:
        answer = answer_question_with_gemini(question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "answer": f"Error in QnA: {str(e)}"})


@app.post("/explain/")
async def post_explain_topic(payload: ExplainRequest):
    """
    Generates a simple, school-student friendly explanation using the local Hugging Face LaMini-Flan-T5 model.
    """
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    try:
        explanation = explain_topic(topic)
        return {"topic": topic, "explanation": explanation}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "topic": topic, "explanation": f"Error: {str(e)}"})


@app.post("/summarize/")
async def post_summarize_text(payload: SummarizeRequest):
    """
    Summarizes a paragraph in simple language using Google Gemini 1.5 Pro.
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "summary": f"Error: {str(e)}"})


@app.post("/quiz")
async def post_generate_quiz(payload: QuizRequest):
    """
    Generates exactly 3 MCQs with 4 options and answers from a given text passage using Gemini.
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        quiz = generate_quiz(text)
        return {"quiz": quiz}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "quiz": []})


@app.get("/learn/recommendations")
async def get_learning_path(topic: str = Query(..., min_length=1, description="Topic or domain for learning recommendations")):
    """
    Generates a structured learning path with Beginner, Intermediate, and Advanced milestones using Gemini.
    """
    topic_clean = topic.strip()
    if not topic_clean:
        raise HTTPException(status_code=400, detail="Topic parameter cannot be empty.")
    try:
        recommendation = get_learning_recommendations(topic_clean)
        return {"topic": topic_clean, "recommendation": recommendation}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "topic": topic_clean, "recommendation": f"Error: {str(e)}"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
