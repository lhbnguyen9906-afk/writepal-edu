from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation

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
    convs = db.query(Conversation).all()

    return [{"id": c.id} for c in convs]