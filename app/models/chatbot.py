from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    message_type: str = Field(default="text")  # text, audio, image


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: str
    user_id: str
    is_user: bool
    emotion_data: Optional[Dict[str, Any]] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message: ChatMessage
    suggestions: Optional[List[str]] = []
    mood_analysis: Optional[Dict[str, Any]] = {}


class ChatHistory(BaseModel):
    messages: List[ChatMessage]
    total: int
    page: int
    size: int 