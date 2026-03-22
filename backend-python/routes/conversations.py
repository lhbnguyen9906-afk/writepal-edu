from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation
from schemas import ConversationCreate

router = APIRouter()


@router.post("/conversations")
def create_conversation(req: ConversationCreate, db: Session = Depends(get_db)):

    conv = Conversation(user_id=req.user_id)

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {"conversation_id": conv.id}