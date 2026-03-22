from pydantic import BaseModel

# =========================
# CHAT
# =========================
class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    mode: str


# =========================
# CONVERSATION
# =========================
class ConversationCreate(BaseModel):
    user_id: int