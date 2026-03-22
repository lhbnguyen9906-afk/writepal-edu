from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

from google import genai
from dotenv import load_dotenv
import os

# 🔥 Load ENV
load_dotenv()

# 🔥 Init Gemini client (API mới)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

router = APIRouter()


# 🧠 Memory (lấy 30 messages gần nhất)
def get_history(db: Session, conversation_id: int):
    msgs = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    history = []
    for m in msgs[-30:]:
        role = "User" if getattr(m, "role", "") == "user" else "Assistant"
        content = getattr(m, "content", "").strip()
        history.append(f"{role}: {content}")

    return "\n".join(history)


# 🎯 Prompt builder (WritePal-Edu)
def build_prompt(req: ChatRequest, history: str):
    return f"""
You are WritePal-Edu, an AI academic writing assistant designed for university students.

Your job:
- Help users improve writing skills
- Explain clearly and simply
- Give structured feedback
- Be supportive but insightful

Mode: {req.mode}
Language: {req.language}

Instructions by mode:
- tutor → explain mistakes, ask guiding questions
- structure → analyze essay structure
- outline → generate outline
- rewrite → rewrite with improvements + explanation

Conversation:
{history}

User input:
"{req.text}"
"""


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # 🔹 1. Save user message
    db.add(Message(
        conversation_id=req.conversation_id,
        role="user",
        content=req.text
    ))
    db.commit()

    # 🔹 2. Get history
    history = get_history(db, req.conversation_id)

    # 🔹 3. Build prompt
    prompt = build_prompt(req, history)

    # 🔹 4. Call Gemini
    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = res.text if hasattr(res, "text") and res.text else "⚠️ Empty response"

    except Exception as e:
        reply = f"⚠️ AI error: {str(e)}"

    # 🔹 5. Save assistant message
    db.add(Message(
        conversation_id=req.conversation_id,
        role="assistant",
        content=reply
    ))
    db.commit()

    # 🔹 6. Return response
    return {"response": reply}