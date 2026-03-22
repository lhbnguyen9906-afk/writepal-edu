from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation, Message

router = APIRouter()


@router.post("/conversations")
def create_conversation(db: Session = Depends(get_db)):
    conv = Conversation(user_id=1)

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {"conversation_id": conv.id}


@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()


@router.get("/conversations/{conv_id}/messages")
def get_messages(conv_id: int, db: Session = Depends(get_db)):
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .all()
    )

    return [{"role": m.role, "content": m.content} for m in msgs]