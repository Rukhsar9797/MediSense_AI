
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

client = Groq(api_key=os.environ["GROQ_API_KEY"])

model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are MediSense AI, an assistant for medication "
                    "adherence habits and general wellness. Never diagnose "
                    "conditions or recommend changing medication doses."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Give me three practical ways to remember daily routines. "
                    "Keep the answer concise."
                ),
            },
        ],
        max_tokens=150,
    )

    print("\nGroq response:\n")
    print(response.choices[0].message.content)

except Exception as exc:
    print("Request failed:", type(exc).__name__, str(exc))