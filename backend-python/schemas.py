from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    mode: str | None = "vi_en"


class PreSurveyCreate(BaseModel):
    user_id: int
    level: str
    goal: str


class ConversationCreate(BaseModel):
    pass