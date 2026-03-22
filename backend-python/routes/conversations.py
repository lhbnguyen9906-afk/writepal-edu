from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation, Message

router = APIRouter()

# =========================
# CREATE
# =========================
@router.post("/conversations")
def create_conversation(db: Session = Depends(get_db)):
    conv = Conversation(user_id=1)

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {"conversation_id": conv.id}


# =========================
# GET ALL
# =========================
@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).all()

    return [{"id": c.id} for c in convs]


# =========================
# GET MESSAGES (FIX 404)
# =========================
@router.get("/conversations/{conv_id}/messages")
def get_messages(conv_id: int, db: Session = Depends(get_db)):
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return [
        {
            "role": m.role,
            "content": m.content
        }
        for m in msgs
    ]


# =========================
# DELETE
# =========================
@router.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conv)
    db.commit()

    return {"message": "Deleted"}