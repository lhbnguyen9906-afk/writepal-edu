from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

from google import genai
from dotenv import load_dotenv
import os

# =========================
# INIT
# =========================
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

router = APIRouter()


# =========================
# MEMORY
# =========================
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


# =========================
# PROMPT
# =========================
def build_prompt(req: ChatRequest, history: str):
    return f"""
You are WritePal-Edu, an AI academic writing assistant for university students.

Mode: {req.mode}
Language: {req.language}

Conversation:
{history}

User:
"{req.text}"

Respond in this format:

### 🧠 Insight

### 🔍 Suggestions
- ...

### ✏️ Try this
"""


# =========================
# API
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # ❗ tránh input rỗng
    if not req.text.strip():
        return {"response": "⚠️ Empty input"}

    # 1. save user
    db.add(Message(
        conversation_id=req.conversation_id,
        role="user",
        content=req.text
    ))
    db.commit()

    # 2. history
    history = get_history(db, req.conversation_id)

    # 3. prompt
    prompt = build_prompt(req, history)

    # =========================
    # 4. CALL GEMINI (SAFE)
    # =========================
    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = None

        # ưu tiên res.text
        if hasattr(res, "text") and res.text:
            reply = res.text

        # fallback candidates
        elif hasattr(res, "candidates") and res.candidates:
            try:
                candidate = res.candidates[0]

                if (
                    hasattr(candidate, "content")
                    and candidate.content
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    reply = candidate.content.parts[0].text

            except Exception:
                reply = None

        # fallback cuối
        if not reply:
            reply = "⚠️ Empty response"

    except Exception as e:
        print("GEMINI ERROR:", e)
        reply = "⚠️ AI temporarily unavailable"

    # 5. save assistant
    db.add(Message(
        conversation_id=req.conversation_id,
        role="assistant",
        content=reply
    ))
    db.commit()

    # 6. return
    return {"response": reply}