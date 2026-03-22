print("🔥 CHAT API NEW VERSION RUNNING")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

# pyright: reportPrivateImportUsage=false
import google.generativeai as genai

from dotenv import load_dotenv
import os

router = APIRouter()

# =========================
# INIT AI (SAFE)
# =========================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY not found")
    model = None
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")


# =========================
# MEMORY
# =========================
def get_history(db: Session, conversation_id: int):
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    history = []
    for m in msgs[-30:]:
        role = "User" if str(m.role) == "user" else "Assistant"
        history.append(f"{role}: {m.content}")

    return "\n".join(history)


# =========================
# CHAT API
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="AI not configured")

        mode = req.mode or "vi_en"
        history = get_history(db, req.conversation_id)

        prompt = f"""
You are WritePal-Edu.

Mode: {mode}

History:
{history}

User:
{req.message}

Answer:
"""

        response = model.generate_content(prompt)

        if not response or not response.text:
            raise ValueError("Empty response from AI")

        answer = response.text

        db.add(Message(
            conversation_id=req.conversation_id,
            role="user",
            content=req.message
        ))

        db.add(Message(
            conversation_id=req.conversation_id,
            role="assistant",
            content=answer
        ))

        db.commit()

        return {"response": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))