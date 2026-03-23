from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    mode: str


class ConversationCreate(BaseModel):
    user_id: int