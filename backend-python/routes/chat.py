from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

import os
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

# =========================
# INIT
# =========================
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # type: ignore

# 👉 MODEL MỚI
model = genai.GenerativeModel("gemini-2.5-flash")  # type: ignore

router = APIRouter()


# =========================
# GET HISTORY
# =========================
def get_history(db, conversation_id):
    msgs = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    history = []
    for m in msgs:
        role = "user" if m.role == "user" else "assistant"
        history.append(f"{role}: {m.content}")

    return "\n".join(history[-6:])


# =========================
# BUILD PROMPT
# =========================
def build_prompt(history, user_input, mode="tutor", language="en"):

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


# =========================
# API CHAT
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # 1. lưu user message
    db.add(Message(
        conversation_id=req.conversation_id,
        role="user",
        content=req.text
    ))
    db.commit()

    # 2. lấy history
    history = get_history(db, req.conversation_id)

    # 3. build prompt
    prompt = build_prompt(
        history,
        req.text,
        getattr(req, "mode", "tutor"),
        getattr(req, "language", "en")
    )

    try:
        # 4. gọi Gemini
        res = model.generate_content(prompt)
        reply = res.text if res and res.text else "⚠️ No response"

    except Exception as e:
        print("GEMINI ERROR:", e)
        reply = f"⚠️ AI unavailable: {str(e)}"

    # 5. lưu bot reply
    db.add(Message(
        conversation_id=req.conversation_id,
        role="assistant",
        content=reply
    ))
    db.commit()

    return {"response": reply}