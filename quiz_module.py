import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
from qna import get_gemini_model, extract_response_text

load_dotenv()

def clean_json_block(text: str) -> str:
    """
    Cleans markdown JSON code blocks (```json ... ``` or ``` ... ```)
    and trims whitespace to produce valid JSON text.
    """
    if not text:
        return ""
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    match = re.search(r"(\[.*\])", cleaned, re.DOTALL)
    if match:
        return match.group(1).strip()
    return cleaned.strip()

def generate_quiz(text: str) -> list:
    """
    Generates exactly 3 multiple-choice questions (MCQs) based on the provided passage.
    Returns a list of dicts with keys: 'question', 'options' (4 items), and 'answer'.
    """
    if not text or not text.strip():
        raise ValueError("Please provide a passage or topic to generate a quiz.")

    t_clean = text.strip()
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.6-flash",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-3.8-flash",
        "gemini-3.7-flash"
    ]
    prompt = f"""You are an educational quiz master for EduGenie.
Generate exactly 3 high-quality multiple choice questions (MCQs) based strictly on the following text passage:

Passage:
{t_clean}

Requirements:
1. Output MUST be ONLY a raw JSON array containing exactly 3 question objects (no markdown, no extra commentary).
2. Each question object MUST have the following structure:
   {{
       "question": "The question string",
       "options": ["Option A", "Option B", "Option C", "Option D"],
       "answer": "The exact string matching one of the 4 options above"
   }}
3. Ensure the questions test understanding and accuracy.
"""

    for model_name in candidate_models:
        model = get_gemini_model(model_name)
        if model:
            try:
                response = model.generate_content(prompt)
                raw_text = extract_response_text(response)
                cleaned_json = clean_json_block(raw_text)
                quiz_data = json.loads(cleaned_json)
                
                if not isinstance(quiz_data, list):
                    if isinstance(quiz_data, dict) and "quiz" in quiz_data:
                        quiz_data = quiz_data["quiz"]
                    elif isinstance(quiz_data, dict) and "questions" in quiz_data:
                        quiz_data = quiz_data["questions"]
                    else:
                        quiz_data = [quiz_data]

                validated_quiz = []
                for item in quiz_data:
                    if isinstance(item, dict) and "question" in item and "options" in item and "answer" in item:
                        options = [str(opt) for opt in item["options"]]
                        validated_quiz.append({
                            "question": str(item["question"]),
                            "options": options,
                            "answer": str(item["answer"])
                        })
                if len(validated_quiz) >= 1:
                    return validated_quiz[:3]
            except Exception as e:
                print(f"Gemini API error in generate_quiz with {model_name}: {e}")
                continue

    # Educational fallback quiz generated from passage keywords
    words = [w for w in re.findall(r'\b[A-Za-z]{4,}\b', t_clean)]
    keyword = words[0].capitalize() if words else "Subject"
    secondary = words[1].capitalize() if len(words) > 1 else "Concept"
    
    return [
        {
            "question": f"Based on the provided passage, what is the primary focus regarding '{keyword}'?",
            "options": [
                f"It explains the core mechanisms and significance of {keyword}",
                f"It proves {keyword} is completely unrelated to the topic",
                f"It demonstrates that {keyword} was discovered in ancient times only",
                f"It argues against the importance of studying {keyword}"
            ],
            "answer": f"It explains the core mechanisms and significance of {keyword}"
        },
        {
            "question": f"Which of the following best reflects the key idea associated with '{secondary}'?",
            "options": [
                f"It acts as an essential supporting component for {keyword}",
                f"It contradicts all known principles of the domain",
                f"It is an obsolete concept with no modern relevance",
                f"It only applies under extreme laboratory conditions"
            ],
            "answer": f"It acts as an essential supporting component for {keyword}"
        },
        {
            "question": f"What can be concluded from reading this excerpt?",
            "options": [
                "Understanding fundamental concepts enables deeper learning and mastery",
                "No factual conclusions can be drawn from the text",
                "The passage suggests stopping further study of the topic",
                "All details mentioned are purely fictional"
            ],
            "answer": "Understanding fundamental concepts enables deeper learning and mastery"
        }
    ]
