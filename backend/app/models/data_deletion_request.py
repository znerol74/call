from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class DataDeletionRequest(Base):
    __tablename__ = "data_deletion_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Request details
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Status: pending, in_progress, completed, failed
    status = Column(String(50), default="pending", nullable=False)

    # Notes
    notes = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="data_deletion_requests")
