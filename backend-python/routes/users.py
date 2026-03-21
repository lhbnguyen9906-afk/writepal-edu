from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate

router = APIRouter()


@router.post("/users")
def create_user(data: UserCreate, db: Session = Depends(get_db)):

    user = User(name=data.name, email=data.email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user_id": user.id}