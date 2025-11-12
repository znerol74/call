from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConversationBase(BaseModel):
    caller_phone_number: str
    direction: str  # inbound, outbound


class ConversationCreate(ConversationBase):
    agent_id: int
    phone_number_id: Optional[int] = None
    call_sid: Optional[str] = None


class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    agent_id: int
    phone_number_id: Optional[int] = None
    call_sid: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    consent_recorded: bool
    caller_consented: bool
    status: str

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    role: str  # user, assistant, system
    content: str


class MessageCreate(MessageBase):
    conversation_id: int
    audio_url: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    audio_url: Optional[str] = None
    timestamp: datetime
    anonymized: bool

    class Config:
        from_attributes = True


class CallLogResponse(BaseModel):
    id: int
    conversation_id: int
    duration: Optional[float] = None
    status: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    retention_until: datetime

    class Config:
        from_attributes = True
