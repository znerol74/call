from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    phone_number_id = Column(Integer, ForeignKey("phone_numbers.id", ondelete="SET NULL"), nullable=True)

    # Call information
    caller_phone_number = Column(String(50), nullable=False)
    call_sid = Column(String(255), unique=True, nullable=True, index=True)  # Twilio Call SID

    # Call direction
    direction = Column(String(20), nullable=False)  # inbound, outbound

    # Timestamps
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)

    # GDPR consent
    consent_recorded = Column(Boolean, default=False, nullable=False)
    caller_consented = Column(Boolean, default=False, nullable=False)

    # Status
    status = Column(String(50), default="active", nullable=False)  # active, completed, failed, transferred

    # Relationships
    user = relationship("User", back_populates="conversations")
    agent = relationship("Agent", back_populates="conversations")
    phone_number = relationship("PhoneNumber", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    call_log = relationship("CallLog", back_populates="conversation", uselist=False, cascade="all, delete-orphan")
