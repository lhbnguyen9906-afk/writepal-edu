from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Message
from schemas import ChatRequest

from google import genai
from dotenv import load_dotenv
import os

router = APIRouter()

print("🔥 CHAT API SAFE VERSION")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 🔥 KHÔNG CRASH NỮA
if not api_key:
    print("⚠️ GOOGLE_API_KEY not found")
    client = None
else:
    client = genai.Client(api_key=api_key)


def get_history(db: Session, conversation_id: int) -> str:
    msgs: List[Message] = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    lines = []
    for m in msgs[-30:]:
        role: str = m.role
        content: str = m.content

        speaker = "User" if role == "user" else "Assistant"
        lines.append(f"{speaker}: {content}")

    return "\n".join(lines)


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="AI not configured")

        history = get_history(db, req.conversation_id)

        prompt = f"""
You are WritePal-Edu.

History:
{history}

User:
{req.message}

Answer:
"""

        print("🔥 GEMINI CALLED")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

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
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))