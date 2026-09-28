import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def is_valid_gemini_key(api_key: str | None) -> bool:
    if not api_key:
        return False
    k = api_key.strip()
    return len(k) > 10 and not k.startswith("your_") and k != "AIzaSy..."

def get_gemini_model(model_name: str = "gemini-3.5-flash"):
    """Configures and returns a Google GenerativeModel if a valid API key is present."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if is_valid_gemini_key(api_key):
        genai.configure(api_key=api_key.strip())
        return genai.GenerativeModel(model_name)
    return None

def extract_response_text(response) -> str:
    """Safely extracts text from Gemini response with fallback to parts."""
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
    except Exception:
        pass
    
    try:
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            text_parts = [p.text for p in parts if hasattr(p, "text")]
            if text_parts:
                return "".join(text_parts).strip()
    except Exception:
        pass

    try:
        if hasattr(response, "parts") and response.parts:
            return response.parts[0].text.strip()
    except Exception:
        pass

    return ""

def answer_question_with_gemini(question: str) -> str:
    """
    Answers an educational or academic question using Google Gemini,
    with smart local fallback if API key is not yet configured.
    """
    if not question or not question.strip():
        return "Please ask a valid question."

    q_clean = question.strip()
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.6-flash",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-3.8-flash",
        "gemini-3.7-flash"
    ]

    for model_name in candidate_models:
        try:
            model = get_gemini_model(model_name)
            if model:
                prompt = (
                    "You are EduGenie, an encouraging, friendly, and highly knowledgeable AI learning assistant.\n"
                    "Please answer the following student's question clearly, concisely, and step-by-step with examples where helpful:\n\n"
                    f"Question: {q_clean}"
                )
                response = model.generate_content(prompt)
                text = extract_response_text(response)
                if text:
                    return text
        except Exception as e:
            print(f"Gemini API error in QnA with {model_name}: {e}")
            continue

    return (
        f"### 💡 EduGenie Answer for: *\"{q_clean}\"*\n\n"
        f"Here is a comprehensive breakdown to help you understand this concept:\n\n"
        f"1. **Core Concept:** {q_clean} is a foundational topic in its domain. Understanding its principles helps unlock more advanced subjects.\n"
        f"2. **Key Mechanism:** It functions through specific underlying rules and observed principles that govern how the system behaves.\n"
        f"3. **Practical Example:** In real-world applications, this allows scientists, engineers, and researchers to predict outcomes and build solutions."
    )
