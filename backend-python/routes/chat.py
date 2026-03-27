from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Message
from schemas import ChatRequest

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        if not req.conversation_id:
            raise HTTPException(status_code=400, detail="Missing conversation_id")

        if not req.message:
            raise HTTPException(status_code=400, detail="Empty message")

        # 🔥 TEST AI (ổn định 100%)
        answer = f"Echo: {req.message}"

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
        print("🔥 ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))