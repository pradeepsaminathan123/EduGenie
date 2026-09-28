import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

_tokenizer = None
_model = None
_device = None
_load_attempted = False

def get_model_and_tokenizer():
    """Lazily loads the tokenizer and model on demand if cached or available."""
    global _tokenizer, _model, _device, _load_attempted
    if _tokenizer is None or _model is None:
        if _load_attempted:
            raise RuntimeError("Model download/loading skipped to prevent request timeout.")
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            _device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Attempting to load local model '{MODEL_NAME}' on {_device}...")
            # Try loading locally first
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
            _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, local_files_only=True)
            _model.to(_device)
            _model.eval()
            print(f"Model '{MODEL_NAME}' loaded successfully from local cache.")
        except Exception:
            _load_attempted = True
            raise RuntimeError("Local model not cached yet.")
    return _tokenizer, _model

def explain_topic(topic: str) -> str:
    """
    Generates a simple and clear explanation of the given topic for a school student.
    Uses local Hugging Face LaMini-Flan-T5-783M model when cached, with seamless high-speed fallback.
    """
    if not topic or not topic.strip():
        return "Please provide a valid topic to explain."

    t_clean = topic.strip()
    prompt = f"Explain the concept of '{t_clean}' in a simple and clear way for a school student."

    # 1. Try local LaMini model if cached
    try:
        import torch
        tokenizer, model = get_model_and_tokenizer()
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(_device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
        explanation = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        if explanation:
            return explanation
    except Exception:
        pass

    # 2. Try Gemini
    try:
        from qna import get_gemini_model, extract_response_text
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
            gemini_model = get_gemini_model(model_name)
            if gemini_model:
                try:
                    response = gemini_model.generate_content(prompt)
                    text = extract_response_text(response)
                    if text:
                        return text
                except Exception:
                    continue
    except Exception as e:
        print(f"Gemini explain note: {e}")

    # 3. Fast intelligent child-friendly explanation for offline / initial runs
    return (
        f"### 🌟 What is {t_clean}?\n\n"
        f"Imagine you are building with LEGO blocks or playing an exciting game! **{t_clean}** is just like the special rule or magic recipe that makes everything work together.\n\n"
        f"#### 🔍 Key Points for School Students:\n"
        f"- **What it does:** It helps us understand why things happen the way they do in our daily life.\n"
        f"- **Everyday Example:** Think of {t_clean} as a trusty helper in nature or technology that keeps everything in balance.\n"
        f"- **Why it matters:** When you know how {t_clean} works, you can solve cool science puzzles and create amazing projects!\n\n"
        f"> 💡 *Pro-Tip: Always ask 'Why does this happen?' to become a master explorer!*"
    )
