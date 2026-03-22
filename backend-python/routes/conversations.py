from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Conversation

router = APIRouter()


@router.post("/conversations")
def create_conversation(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):

    convo = Conversation(user_id=user_id)
    db.add(convo)
    db.commit()
    db.refresh(convo)

    return {"conversation_id": convo.id}