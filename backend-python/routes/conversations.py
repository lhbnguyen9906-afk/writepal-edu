from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation, Message

router = APIRouter()


@router.post("/conversations")
def create_conversation(db: Session = Depends(get_db)):
    convo = Conversation(title="New Chat")
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return {"id": convo.id, "title": convo.title}


@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()


@router.get("/conversations/{id}/messages")
def get_messages(id: int, db: Session = Depends(get_db)):

    msgs = db.query(Message).filter(
        Message.conversation_id == id
    ).order_by(Message.created_at.asc()).all()

    return [
        {
            "sender": "user" if str(m.role) == "user" else "bot",
            "text": m.content
        }
        for m in msgs
    ]