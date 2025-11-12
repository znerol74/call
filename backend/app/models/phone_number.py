from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=True, index=True)

    phone_number = Column(String(50), unique=True, nullable=False, index=True)

    # Twilio configuration
    provider = Column(String(50), default="twilio", nullable=False)
    provider_config = Column(JSON, nullable=True)  # Additional provider-specific config

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="phone_numbers")
    agent = relationship("Agent", back_populates="phone_numbers")
    conversations = relationship("Conversation", back_populates="phone_number", cascade="all, delete-orphan")
