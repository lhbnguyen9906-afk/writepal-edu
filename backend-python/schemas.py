from pydantic import BaseModel
from pydantic import BaseModel

class PreSurveyCreate(BaseModel):
    user_id: int
    level: str
    goal: str

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    mode: str


class ConversationCreate(BaseModel):
    user_id: int