from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: int
    text: str
    user_id: int
    mode: str = "tutor"
    language: str = "en"


class UserCreate(BaseModel):
    name: str
    email: str


class PreSurveyCreate(BaseModel):
    user_id: int
    level: str
    goal: str