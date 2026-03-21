from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

router = APIRouter()


def get_history(db, conversation_id):
    msgs = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    history = []
    for m in msgs:
        role = "user" if str(m.role) == "user" else "assistant"
        history.append(f"{role}: {m.content}")

    return "\n".join(history[-6:])


def build_prompt(history, user_input, mode, language):

    if language == "vi":
        lang = "Giải thích bằng tiếng Việt. KHÔNG đưa đáp án hoàn chỉnh."
    else:
        lang = "Explain in English. DO NOT give full answers."

    return f"""
You are WritePal-Edu, a guided writing tutor.

Conversation:
{history}

Student:
"{user_input}"

Mode: {mode}

{lang}

Rules:
- Give hints only
- Ask 2–4 questions
- Do NOT rewrite full answer

Format:

### 🧠 Insight

### 🔍 Think about this
- question
- question

### ✏️ Your Turn
"""


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    db.add(Message(
        conversation_id=req.conversation_id,
        role="user",
        content=req.text
    ))
    db.commit()

    history = get_history(db, req.conversation_id)

    prompt = build_prompt(history, req.text, req.mode, req.language)

    try:
        res = model.generate_content(prompt)
        reply = res.text
    except Exception:
        reply = "⚠️ AI unavailable"

    db.add(Message(
        conversation_id=req.conversation_id,
        role="assistant",
        content=reply
    ))
    db.commit()

    return {"response": reply}