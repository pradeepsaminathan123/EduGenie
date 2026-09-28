import os
from dotenv import load_dotenv
import google.generativeai as genai
from qna import get_gemini_model, extract_response_text

load_dotenv()

def get_learning_recommendations(topic: str) -> str:
    """
    Generates a comprehensive, structured learning path for any given topic using Gemini 1.5 Pro,
    with smart structured roadmap fallback if API key is not yet configured.
    """
    if not topic or not topic.strip():
        return "Please specify a topic or skill to generate a learning path."

    t_clean = topic.strip()
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.6-flash",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-3.8-flash",
        "gemini-3.7-flash"
    ]
    prompt = f"""You are an expert AI tutor and curriculum designer for EduGenie.
Create a well-structured, inspiring, step-by-step learning roadmap for the following topic: "{t_clean}".

Please format the response with clean markdown headings, bullet points, and emojis matching this structure:

### 🎯 Roadmap Overview
A brief summary of what the learner will master.

---

### 🟢 1. Beginner Level (1-2 Weeks)
- **Key Concepts to Master:**
- **Recommended Hands-on Tutorials & Video Channels:**
- **Recommended Books & Beginner Docs:**
- **Practical Milestone Project:**

---

### 🟡 2. Intermediate Level (2-3 Weeks)
- **Key Concepts to Master:**
- **Recommended Deep-Dive Resources & Tutorials:**
- **Practice Platforms & Coding Challenges:**
- **Practical Milestone Project:**

---

### 🔴 3. Advanced Level (3-4+ Weeks)
- **Key Concepts & System Architecture:**
- **Advanced Case Studies, Books & Research Papers:**
- **Top Practice Platforms & Open-Source Contributions:**
- **Capstone Project Idea:**

---

### 💡 Pro-Tips for Accelerated Learning
Top 3 actionable habits for mastering this field effectively.
"""

    for model_name in candidate_models:
        model = get_gemini_model(model_name)
        if model:
            try:
                response = model.generate_content(prompt)
                recommendation = extract_response_text(response)
                if recommendation:
                    return recommendation.strip()
            except Exception as e:
                print(f"Gemini API error in get_learning_recommendations with {model_name}: {e}")
                continue

    # Structured learning roadmap fallback
    return f"""### 🎯 Roadmap Overview: Mastering {t_clean}
This curriculum provides a structured, phased roadmap to guide you from foundational knowledge to complete subject mastery.

---

### 🟢 1. Beginner Level (1-2 Weeks)
- **Key Concepts to Master:** Core terminology, syntax, basic mental models, and environment setup for {t_clean}.
- **Recommended Hands-on Tutorials & Video Channels:** YouTube beginner playlists, freeCodeCamp, CrashCourse, and official introductory guides.
- **Recommended Books & Beginner Docs:** Getting Started with {t_clean} handbook and beginner-friendly cheatsheets.
- **Practical Milestone Project:** Build a "Hello World" interactive demo or foundational mini-project.

---

### 🟡 2. Intermediate Level (2-3 Weeks)
- **Key Concepts to Master:** Data flow, state management, algorithmic thinking, and modular design patterns.
- **Recommended Deep-Dive Resources & Tutorials:** Interactive sandboxes, official documentation, and community code walkthroughs.
- **Practice Platforms & Coding Challenges:** LeetCode, HackerRank, Exercism, or subject-specific quizzes.
- **Practical Milestone Project:** Develop a functional, multi-feature application implementing real data.

---

### 🔴 3. Advanced Level (3-4+ Weeks)
- **Key Concepts & System Architecture:** Performance optimization, edge cases, scalability, security, and production best practices.
- **Advanced Case Studies & Research Papers:** Architecture blueprints, engineering blogs, and seminal domain papers.
- **Top Practice Platforms & Open-Source:** Contribute to GitHub open-source repositories and join developer communities.
- **Capstone Project Idea:** End-to-end full stack project incorporating automation and deployment.

---

### 💡 Pro-Tips for Accelerated Learning
1. **Build in Public:** Teach what you learn through notes or blog posts.
2. **Active Recall:** Take short quizzes right after reading new concepts.
3. **Daily Consistency:** Dedicate 45 focused minutes daily rather than weekend cramming.
"""
