from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class PhoneNumberBase(BaseModel):
    phone_number: str
    provider: str = "twilio"
    provider_config: Optional[Dict[str, Any]] = None


class PhoneNumberCreate(PhoneNumberBase):
    agent_id: Optional[int] = None


class PhoneNumberUpdate(BaseModel):
    agent_id: Optional[int] = None
    provider_config: Optional[Dict[str, Any]] = None


class PhoneNumberResponse(PhoneNumberBase):
    id: int
    user_id: int
    agent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
