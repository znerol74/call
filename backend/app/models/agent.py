from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)
    greeting_message = Column(Text, nullable=False)

    # Voice configuration
    voice_id = Column(String(255), nullable=True)  # ElevenLabs voice ID
    voice_provider = Column(String(50), default="elevenlabs", nullable=False)  # elevenlabs, coqui, etc.

    # Language
    language = Column(String(10), default="de", nullable=False)  # de, en, etc.

    # Tools configuration (JSON array of tool definitions)
    tools_config = Column(JSON, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="agents")
    phone_numbers = relationship("PhoneNumber", back_populates="agent", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="agent", cascade="all, delete-orphan")
