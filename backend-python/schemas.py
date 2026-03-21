from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class PreSurveyCreate(BaseModel):
    user_id: int
    level: str
    goal: str


class ChatRequest(BaseModel):
    conversation_id: int
    text: str
    mode: str = "tutor"
    language: str = "en"