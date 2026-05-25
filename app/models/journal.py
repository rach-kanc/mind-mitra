from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JournalEntryBase(BaseModel):
    mood: int
    text: str
    date: Optional[datetime] = None

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntry(JournalEntryBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True 