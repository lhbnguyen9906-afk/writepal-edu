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
load_dotenv() # lệnh này không chạy được trên github chỉ chạy ở localhost thô

#api_key = os.getenv("GEMINI_API_KEY") # dán key của gemini 
# debug
#if not api_key:
#    raise Exception("❌ GEMINI_API_KEY not found in environment")

#print("API KEY:", api_key)  # debug
#if not api_key:
#    print("⚠️ NO API KEY 02")
#    client = None
#else:
#    client = genai.Client(api_key=api_key)


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

#debug get key
@router.get("/debug-env")
def debug_env():
    import os
    return {"key": os.getenv("GEMINI_API_KEY")}
# =========================
# CHAT
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    #
    api_key = os.getenv("GEMINI_API_KEY")

    print("API KEY:", api_key)

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="❌ GEMINI_API_KEY not found"
        )

    client = genai.Client(api_key=api_key)
    #
    if client is None:
        #raise HTTPException(status_code=500, detail="AI not configured,"+api_key)
        raise HTTPException(
            status_code=500,
            detail=f"AI not configured, api_key={api_key}"
        )

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
You are WritePal-Edu — a Socratic writing tutor.

Conversation:
{history}

User follow-up:
{message}

IMPORTANT:
- This is NOT a new essay
- This is a follow-up
- Do NOT repeat full feedback

TASK:
- Answer briefly (2–4 sentences)
- Refer to previous feedback if relevant
- Guide the student using questions
- Avoid giving direct corrections unless asked
- {lang_instruction}

STYLE:
- Be concise
- Focus on helping the student think
"""
    else:
        prompt = f"""
You are WritePal-Edu — a writing tutor.

Essay:
{message}
IMPORTANT:
- The user is asking for direct corrections, but you should NOT give them immediately

RULES:
- {lang_instruction}
- Keep quoted sentences in original language
- Do NOT rewrite the full essay
- Do NOT give direct corrections immediately
- Use guiding questions instead of direct answers

TASK:
- Provide corrected version
- Briefly explain why (1–2 sentences)
- {lang_instruction}

Structure Snapshot:
- Briefly describe overall organization (2–3 sentences)

What to Fix First:
- Priority 1:
- Priority 2:
- Priority 3:

Error Awareness:
(choose 2–3 sentences from the essay)
- Quote the sentence
- Ask 2–3 guiding questions for each
- Do NOT give corrected version

Deep Thinking Questions:
1.
2.
3.

Stretch Task:
- Suggest ONE improvement

Focus for Revision:
1.
2.
3.

Key Insight:
(1–2 sentences)

STYLE:
- Be clear, structured, concise
- Focus on clarity and insight
- Avoid generic praise
- Prioritize thinking over correction
"""

    try:
        response = client.models.generate_content(
            #chọn model để trả lời, càng mạnh càng dễ bị quá tải, nên cân nhắc nếu bạn chạy nhiều request
            #model="gemini-2.5-flash", # model chất lượng cao, nhưng dễ bị quá tải
            model="gemini-flash-latest", # dễ bị quá tải
            #model="gemini-1.5-flash", # model nhẹ hơn, ít bị quá tải, nhưng chất lượng thấp hơn
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