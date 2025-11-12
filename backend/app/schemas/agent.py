from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


class AgentBase(BaseModel):
    name: str
    system_prompt: str
    greeting_message: str
    voice_id: Optional[str] = None
    voice_provider: str = "elevenlabs"
    language: str = "de"
    tools_config: Optional[List[ToolDefinition]] = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    voice_id: Optional[str] = None
    voice_provider: Optional[str] = None
    language: Optional[str] = None
    tools_config: Optional[List[ToolDefinition]] = None


class AgentResponse(AgentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
