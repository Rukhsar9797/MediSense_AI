
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


SYSTEM_PROMPT = """
You are MediSense AI, an assistant for medication adherence habits
and general wellness.

Rules:
- Use only the statistics and context supplied to you.
- Never diagnose a medical condition or claim to predict clinical outcomes.
- Never recommend starting, stopping, skipping, doubling, or changing
  prescribed medication doses.
- Offer practical, nonjudgmental habit-building suggestions.
- Encourage the user to ask their pharmacist or clinician about
  medication-specific concerns.
- Do not claim that a reminder or wellness suggestion guarantees adherence.
- Keep responses clear, concise, and supportive.
"""


def _ask_groq(user_prompt: str, max_tokens: int = 350) -> str:
    """Send a prompt to Groq and return a safe fallback on failure."""

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    if not api_key:
        return (
            "AI assistance is unavailable because the Groq API key "
            "is not configured. Please check your local .env file."
        )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.4,
        )

        answer = response.choices[0].message.content
        return answer.strip() if answer else (
            "No AI response was returned. Please try again."
        )

    except Exception:
        # Avoid exposing API keys or technical details in the UI.
        return (
            "AI assistance is temporarily unavailable. "
            "Please try again later. Your calculated adherence "
            "statistics are still available."
        )


def generate_report(stats: dict, risk: dict) -> str:
    """Generate a short summary from calculated patient statistics."""

    prompt = f"""
Create a concise medication-adherence summary using these results.

Adherence statistics:
{stats}

Seven-day rule-based adherence-risk estimate:
{risk}

Include:
1. A brief summary of the measured adherence.
2. The main missed-dose pattern, if the data supports one.
3. Two practical reminder or routine-building suggestions.

Clearly describe the risk score as a prototype heuristic, not a
clinical prediction. Do not invent information that is not supplied.
Do not recommend changing medication doses.
"""
    return _ask_groq(prompt, max_tokens=350)


def get_recommendations(
    question: str,
    preferences=None,
    adherence_summary=None,
) -> str:
    """Answer a wellness or adherence-habit question."""

    prompt = f"""
User's question:
{question}

User-provided preferences:
{preferences if preferences else "None provided"}

Calculated adherence summary:
{adherence_summary if adherence_summary else "None provided"}

Answer the question with practical, general wellness or habit-building
suggestions. Be supportive and concise. Do not invent patient history.
If the question concerns a medication's safety, interactions, or dosage,
recommend consulting a pharmacist or clinician.
"""
    return _ask_groq(prompt, max_tokens=350)