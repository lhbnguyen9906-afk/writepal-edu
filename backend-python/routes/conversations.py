from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Conversation, Message
from schemas import ConversationCreate
from fastapi import HTTPException

router = APIRouter()

# CREATE
@router.post("/conversations")
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    conv = Conversation(
        user_id=1,
        title=data.title or "New Chat"
    )

    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {
        "id": conv.id,
        "title": conv.title
    }

# GET ALL
@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).all()

    return [
        #{"id": c.id, "title": f"Chat {c.id}"}
        {"id": c.id, "title": c.title}
        for c in convs
    ]

# GET MESSAGES
@router.get("/conversations/{conv_id}/messages")
def get_messages(conv_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(
        Message.conversation_id == conv_id
    ).all()

    return [
        {"role": m.role, "content": m.content}
        for m in msgs
    ]
    
# UPDATE
@router.put("/conversations/{conv_id}")
def rename_conversation(
    conv_id: int,
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Not found")

    if data.title is None:
        raise HTTPException(status_code=400, detail="Title is required")

    conv.title = data.title
    db.commit()

    return {"status": "ok"}

# DELETE
@router.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Not found")

    # 🔥 xóa messages trước (quan trọng)
    db.query(Message).filter(
        Message.conversation_id == conv_id
    ).delete()

    db.delete(conv)
    db.commit()

    return {"status": "deleted"}