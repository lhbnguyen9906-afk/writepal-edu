from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import PreSurvey
from schemas import PreSurveyCreate

router = APIRouter()


@router.post("/survey")
def create_survey(data: PreSurveyCreate, db: Session = Depends(get_db)):

    survey = PreSurvey(
        user_id=data.user_id,
        level=data.level,
        goal=data.goal
    )

    db.add(survey)
    db.commit()

    return {"status": "saved"}