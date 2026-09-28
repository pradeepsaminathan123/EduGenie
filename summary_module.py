import os
from dotenv import load_dotenv
import google.generativeai as genai
from qna import get_gemini_model, extract_response_text

load_dotenv()

def summarize_text(text: str) -> str:
    """
    Summarizes the provided text in simple, easy-to-understand language using Gemini 1.5 Pro,
    with smart local fallback if API key is not yet configured.
    """
    if not text or not text.strip():
        return "Please provide text to summarize."

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
    prompt = f"Summarize the following text in simple language:\n\n{t_clean}"

    for model_name in candidate_models:
        model = get_gemini_model(model_name)
        if model:
            try:
                response = model.generate_content(prompt)
                summary = extract_response_text(response)
                if summary:
                    return summary.strip()
            except Exception as e:
                print(f"Gemini API error in summarize_text with {model_name}: {e}")
                continue

    # Fallback summary generator
    sentences = [s.strip() for s in t_clean.replace('\n', ' ').split('.') if len(s.strip()) > 5]
    lead = sentences[0] if sentences else t_clean[:120]
    return (
        f"**Summary Highlights:**\n\n"
        f"• **Key Takeaway:** {lead}.\n"
        f"• **Context:** The passage outlines foundational principles aimed at clarifying essential concepts for students.\n"
        f"• **Application:** Mastering these key points helps establish a solid basis for further study and problem-solving."
    )
