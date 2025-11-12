from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    # Action details
    action = Column(String(100), nullable=False)  # login, logout, create_agent, delete_data, etc.
    resource = Column(String(100), nullable=True)  # agents, phone_numbers, etc.
    resource_id = Column(Integer, nullable=True)

    # Details
    details = Column(JSON, nullable=True)

    # IP address
    ip_address = Column(String(50), nullable=True)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
