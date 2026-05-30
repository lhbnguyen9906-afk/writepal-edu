from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Message
from schemas import ChatRequest
from models import Conversation

from google import genai
from dotenv import load_dotenv
import os

router = APIRouter()
MAX_HISTORY_CHARS = 2000

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
def get_history(db: Session, conversation_id: int) -> str:
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
 
    history_text = "\n".join(history)
 
    # Giới hạn độ dài để tránh vượt token limit
    if len(history_text) > MAX_HISTORY_CHARS:
        history_text = history_text[-MAX_HISTORY_CHARS:]
 
    return history_text

#debug get key
@router.get("/debug-env")
def debug_env():
    import os
    key = os.getenv("GEMINI_API_KEY")
    return {"key_found": bool(key), "key_preview": key[:8] + "..." if key else None}
# =========================
# CHAT
# =========================
@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Load API key mỗi request (Railway inject vào env, không cần load_dotenv)
    api_key = os.getenv("GEMINI_API_KEY")
 
    if not api_key:
        raise HTTPException(status_code=500, detail="❌ GEMINI_API_KEY not found")
 
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to init Gemini client: {str(e)}")
 
    # Kiểm tra conversation tồn tại sớm — tránh lãng phí call Gemini nếu không có
    conv = db.query(Conversation).filter(Conversation.id == req.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    history = get_history(db, req.conversation_id)

    word_count = len(message.split())
    is_followup = len(history) > 0 and word_count < 20
    is_short = word_count < 8
    is_question = "?" in message
    use_vi = is_vietnamese(message)


    if use_vi:
        lang_instruction = (
        "Respond in Vietnamese.\n\n"
        "IMPORTANT:\n"
        "- Maintain the SAME depth, detail, and reasoning as the English version\n"
        "- Do NOT simplify, summarize, or shorten ideas\n"
        "- Preserve all guiding questions and explanations\n"
        "- Keep quoted text in English\n"
        "- Use clear, natural but academically appropriate Vietnamese\n"
        "- The explanation must feel like a real tutor thinking with the student, not a simplified translation"
    )
    else:
        lang_instruction = "Respond in English."
    # =========================
    # PROMPT
    # =========================
    if is_followup or is_short or is_question:
        prompt = f"""
You are WritePal-Edu — a friendly and thoughtful writing tutor.
 
Conversation:
{history}
 
User:
{message}
 
IMPORTANT:
- This is NOT a full essay feedback
- Do NOT give full structured feedback
- Do NOT sound like a report
 
TASK:
- Respond naturally like a real tutor in a conversation
- Keep it short (2–4 sentences)
- Be flexible: answer directly if the question is clear
- If helpful, ask 1 guiding question
- Refer to previous feedback only if relevant
- {lang_instruction}
 
STYLE:
- Conversational, natural, and concise
- No headings, no bullet points
- No generic phrases like "I understand your concern"
- Focus on clarity and usefulness
- Focus on helping the student think
"""
    else:
        prompt = f"""
You are WritePal-Edu — a writing tutor who gives clear corrections AND helps students think deeper.

Essay:
{message}

RULES:
- {lang_instruction}
- Keep quoted sentences in original language
- Do NOT rewrite the full essay
- Be honest and specific — avoid generic praise

STRUCTURE YOUR RESPONSE EXACTLY LIKE THIS:

Structure Snapshot:
- Briefly describe the overall organization (2–3 sentences)

What to Fix First:
- Priority 1: [specific issue + corrected version + 1-sentence explanation why]
- Priority 2: [specific issue + corrected version + 1-sentence explanation why]
- Priority 3: [specific issue + corrected version + 1-sentence explanation why]

Error Awareness:
(choose 2–3 sentences from the essay that need improvement)
For each:
- Quote the original sentence
- Give a corrected version
- Ask 1–2 guiding questions so the student understands WHY it was wrong

Deep Thinking Questions:
1.
2.
3.

Stretch Task:
- Suggest ONE way to make the essay stronger beyond fixing errors

Key Insight:
(1–2 sentences summarizing the most important thing the student should take away)

STYLE:
- Clear, structured, and encouraging
- Corrections must be specific — not vague like "improve your vocabulary"
- Questions should make the student think, not just confirm the answer
- {lang_instruction}
"""

    try:
        response = client.models.generate_content(
            #chọn model để trả lời, càng mạnh càng dễ bị quá tải, nên cân nhắc nếu bạn chạy nhiều request
            model="gemini-2.0-flash", # model chất lượng cao, nhưng dễ bị quá tải
            #model="gemini-flash-latest", # dễ bị quá tải
            #model="gemini-2.0-flash", # model ổn định, chất lượng tốt
            #model="gemini-1.5-flash", # model nhẹ hơn, ít bị quá tải, nhưng chất lượng thấp hơn
            contents=prompt
        )

        # 🔥 SAFE PARSE (KHÔNG CRASH)
        answer = getattr(response, "text", None) or "⚠️ AI did not return text"

    

    except Exception as e:
        print("🔥 Gemini error:", repr(e))
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
 
    # =========================
    # SAVE TO DB
    # =========================
    try:
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
        print("✅ DB COMMIT OK")
 
    except Exception as e:
        print("❌ DB ERROR:", repr(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
 
    return {"response": answer}