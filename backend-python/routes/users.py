from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter()


@router.post("/login")
def login(username: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"user_id": user.id}