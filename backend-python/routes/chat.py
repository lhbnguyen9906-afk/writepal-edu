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
    is_followup = len(message.split()) < 20

    # =========================
    # PROMPT
    # =========================
    if is_followup:
        prompt = f"""
You are WritePal-Edu.

Conversation:
{history}

User question:
{message}

Task:
- Answer briefly (2–4 sentences)
- Clarify previous feedback
- DO NOT repeat full analysis
"""
    else:
        prompt = f"""
You are WritePal-Edu — a writing coach.

Student essay:
{message}

RULES:
- Respond in Vietnamese
- Keep quotes in English
- Do NOT rewrite full essay

TASK:
1. 2 strengths
2. 2 weaknesses (with exact quotes)
3. 3 questions
4. 1 short hint

FORMAT:

🟢 Điểm mạnh:
...

🔴 Cần cải thiện:
(quote English)

🔎 Câu hỏi:
1.
2.
3.

💡 Gợi ý:
...
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text if response.text else "⚠️ No response"

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
        raise HTTPException(status_code=500, detail=str(e))