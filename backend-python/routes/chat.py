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
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# =========================
# MEMORY
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

    if not req.conversation_id:
        raise HTTPException(status_code=400, detail="Missing conversation_id")

    history = get_history(db, req.conversation_id)

    # 🔥 PHÂN BIỆT STATE (INTELLIGENCE)
    is_followup = len(history.split("\n")) > 2

    if not is_followup:
        # =========================
        # 🧠 FIRST RESPONSE (REFLECTION)
        # =========================
      prompt = f"""
You are WritePal-Edu.

Student text:
{req.message}

=========================
STRICT RULES (MANDATORY)
=========================

- DO NOT rewrite the paragraph
- DO NOT repeat the paragraph
- DO NOT summarize
- DO NOT explain everything

If you break rules → response is invalid.

=========================
TASK
=========================

Ask 3 Socratic questions that:
- challenge logic
- identify unclear claims
- push deeper thinking

Then give ONLY 1 short hint.

=========================
FORMAT (STRICT)
=========================

🔎 Questions:
1.
2.
3.

💡 Hint:
...

=========================
ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    answer = response.text

    # =========================
    # SAVE MEMORY
    # =========================
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