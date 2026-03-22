from pydantic import BaseModel
from typing import Optional

# =========================
# CHAT
# =========================
class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    mode: Optional[str] = "vi_en"


# =========================
# CONVERSATION
# =========================
class ConversationCreate(BaseModel):
    user_id: Optional[int] = 1  # 👈 tránh lỗi 422