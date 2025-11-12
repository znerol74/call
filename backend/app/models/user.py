from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # GDPR fields
    consent_timestamp = Column(DateTime, nullable=True)
    data_processing_consent = Column(Boolean, default=False, nullable=False)
    terms_accepted = Column(Boolean, default=False, nullable=False)
    privacy_policy_accepted = Column(Boolean, default=False, nullable=False)

    # Relationships
    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    phone_numbers = relationship("PhoneNumber", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    data_deletion_requests = relationship("DataDeletionRequest", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
