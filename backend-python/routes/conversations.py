from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation

router = APIRouter()

# =========================
# CREATE (FIX 422)
# =========================
@router.post("/conversations")
def create_conversation(db: Session = Depends(get_db)):
    conv = Conversation(user_id=1)  # 👈 fix cứng

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {"conversation_id": conv.id}


# =========================
# GET ALL (FIX 405)
# =========================
@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).all()

    return [
        {
            "id": c.id,
            "user_id": c.user_id
        }
        for c in convs
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