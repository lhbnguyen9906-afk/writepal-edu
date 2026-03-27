from pydantic import BaseModel
from typing import Optional

# =========================
# CHAT
# =========================
class ChatRequest(BaseModel):
    conversation_id: Optional[int]   # 👈 tránh 422
    message: str
    mode: str


# =========================
# CONVERSATION
# =========================
class ConversationCreate(BaseModel):
    user_id: int = 1


# =========================
# SURVEY (optional)
# =========================
class PreSurveyCreate(BaseModel):
    user_id: int
    level: str
    goal: str