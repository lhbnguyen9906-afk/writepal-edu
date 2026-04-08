from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Message
from schemas import ChatRequest

from google import genai
from dotenv import load_dotenv
import os

router = APIRouter()

# =========================
# INIT AI
# =========================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("⚠️ NO API KEY")
    client = None
else:
    client = genai.Client(api_key=api_key)


# =========================
# LANGUAGE DETECTION
# =========================
def is_vietnamese(text):
    return any(c in text for c in "ăâđêôơưáàảãạấầẩẫậ")


# =========================
# HISTORY
# =========================
def get_history(db, conversation_id):
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    history = []
    for m in msgs[-10:]:
        role = "User" if m.role == "user" else "Assistant"
        history.append(f"{role}: {m.content}")

    return "\n".join(history)


# =========================
# CHAT
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    if client is None:
        raise HTTPException(status_code=500, detail="AI not configured")

    message = req.message.strip()
    history = get_history(db, req.conversation_id)

    # 🔥 detect follow-up
    is_followup = len(message.split()) < 20 and len(history) > 0

    # 🔥 detect language
    use_vi = is_vietnamese(message)
    lang_instruction = "Respond in Vietnamese" if use_vi else "Respond in English"

    # =========================
    # PROMPT
    # =========================
    if is_followup:
        prompt = f"""
You are WritePal-Edu.

Conversation:
{history}

User follow-up:
{message}

IMPORTANT:
- This is NOT a new essay
- This is a follow-up

TASK:
- Answer briefly (2–3 sentences)
- Refer to previous feedback
- {lang_instruction}

DO NOT repeat full analysis
"""
    else:
        prompt = f"""
You are WritePal-Edu — a writing tutor.

Essay:
{message}

RULES:
- {lang_instruction}
- Keep quotes in original language
- Do NOT rewrite full essay

TASK:
1. 2 strengths
2. 2 weaknesses (with quotes)
3. 3 questions
4. 1 hint

FORMAT:

🟢 Strengths:
...

🔴 Weaknesses:
(quote original)

🔎 Questions:
1.
2.
3.

💡 Hint:
...
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # 🔥 SAFE PARSE (KHÔNG CRASH)
        answer = getattr(response, "text", None)

        if not answer:
            answer = "⚠️ AI did not return text"

        # SAVE DB
        db.add(Message(
            conversation_id=req.conversation_id,
            role="user",
            content=message
        ))

        db.add(Message(
            conversation_id=req.conversation_id,
            role="assistant",
            content=answer
        ))

        db.commit()

        return {"response": answer}

    except Exception as e:
        print("🔥 ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))