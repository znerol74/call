from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import json
import io

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.agent import Agent
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.call_log import CallLog
from app.models.data_deletion_request import DataDeletionRequest

router = APIRouter()


@router.get("/export")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Export all user data (GDPR Right to Access)"""
    # Collect all user data
    data = {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at.isoformat(),
            "consent_timestamp": current_user.consent_timestamp.isoformat() if current_user.consent_timestamp else None,
            "data_processing_consent": current_user.data_processing_consent,
            "terms_accepted": current_user.terms_accepted,
            "privacy_policy_accepted": current_user.privacy_policy_accepted,
        },
        "agents": [],
        "conversations": [],
    }

    # Get agents
    agents_result = await db.execute(
        select(Agent).where(Agent.user_id == current_user.id)
    )
    agents = agents_result.scalars().all()

    for agent in agents:
        data["agents"].append({
            "id": agent.id,
            "name": agent.name,
            "system_prompt": agent.system_prompt,
            "greeting_message": agent.greeting_message,
            "voice_id": agent.voice_id,
            "voice_provider": agent.voice_provider,
            "language": agent.language,
            "tools_config": agent.tools_config,
            "created_at": agent.created_at.isoformat(),
        })

    # Get conversations
    conversations_result = await db.execute(
        select(Conversation).where(Conversation.user_id == current_user.id)
    )
    conversations = conversations_result.scalars().all()

    for conversation in conversations:
        # Get messages
        messages_result = await db.execute(
            select(Message).where(Message.conversation_id == conversation.id)
        )
        messages = messages_result.scalars().all()

        # Get call log
        call_log_result = await db.execute(
            select(CallLog).where(CallLog.conversation_id == conversation.id)
        )
        call_log = call_log_result.scalar_one_or_none()

        conv_data = {
            "id": conversation.id,
            "caller_phone_number": conversation.caller_phone_number,
            "direction": conversation.direction,
            "start_time": conversation.start_time.isoformat(),
            "end_time": conversation.end_time.isoformat() if conversation.end_time else None,
            "status": conversation.status,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content if not msg.anonymized else "[ANONYMIZED]",
                    "timestamp": msg.timestamp.isoformat(),
                }
                for msg in messages
            ],
        }

        if call_log:
            conv_data["call_log"] = {
                "duration": call_log.duration,
                "status": call_log.status,
                "transcript": call_log.transcript,
                "summary": call_log.summary,
            }

        data["conversations"].append(conv_data)

    # Create JSON file in memory
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    json_bytes = json_str.encode('utf-8')

    # Return as downloadable file
    return StreamingResponse(
        io.BytesIO(json_bytes),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=user_data_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        }
    )


@router.post("/delete-account")
async def request_account_deletion(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request account deletion (GDPR Right to Erasure)"""
    # Check if there's already a pending request
    result = await db.execute(
        select(DataDeletionRequest).where(
            DataDeletionRequest.user_id == current_user.id,
            DataDeletionRequest.status == "pending"
        )
    )
    existing_request = result.scalar_one_or_none()

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deletion request already pending"
        )

    # Create deletion request
    deletion_request = DataDeletionRequest(
        user_id=current_user.id,
        status="pending"
    )

    db.add(deletion_request)
    await db.commit()

    return {
        "message": "Account deletion requested. Your account and all associated data will be deleted.",
        "request_id": deletion_request.id
    }


@router.delete("/delete-account/{request_id}")
async def confirm_account_deletion(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Confirm and execute account deletion"""
    # Get deletion request
    result = await db.execute(
        select(DataDeletionRequest).where(
            DataDeletionRequest.id == request_id,
            DataDeletionRequest.user_id == current_user.id,
            DataDeletionRequest.status == "pending"
        )
    )
    deletion_request = result.scalar_one_or_none()

    if not deletion_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deletion request not found"
        )

    # Update request status
    deletion_request.status = "in_progress"
    await db.commit()

    try:
        # Delete user (cascade will delete all related data)
        await db.delete(current_user)

        # Mark request as completed
        deletion_request.status = "completed"
        deletion_request.completed_at = datetime.utcnow()
        await db.commit()

        return {"message": "Account and all data successfully deleted"}

    except Exception as e:
        deletion_request.status = "failed"
        deletion_request.notes = str(e)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )


@router.get("/privacy-policy")
async def get_privacy_policy():
    """Get privacy policy (GDPR requirement)"""
    return {
        "title": "Privacy Policy",
        "content": """
# Privacy Policy

## 1. Data Controller
CAL - AI Phone Agent Assistant System

## 2. Data We Collect
- Email address and password (hashed)
- AI agent configurations (system prompts, greetings, voice settings)
- Phone call recordings and transcripts
- Call metadata (duration, timestamps, phone numbers)

## 3. Legal Basis for Processing
We process your data based on your explicit consent (GDPR Art. 6(1)(a)).

## 4. Data Retention
- Call recordings: 90 days (configurable)
- Transcripts: 180 days, then anonymized
- Account data: Until account deletion

## 5. Your Rights
- Right to access your data
- Right to rectification
- Right to erasure (deletion)
- Right to data portability
- Right to withdraw consent

## 6. Data Security
All data is encrypted at rest and in transit using industry-standard protocols.

## 7. Contact
For privacy concerns, please contact: [Your Contact Email]

Last updated: """ + datetime.utcnow().strftime('%Y-%m-%d')
    }


@router.get("/terms-of-service")
async def get_terms_of_service():
    """Get terms of service"""
    return {
        "title": "Terms of Service",
        "content": """
# Terms of Service

## 1. Acceptance of Terms
By using CAL, you agree to these terms.

## 2. Service Description
CAL provides AI-powered phone agent services.

## 3. User Responsibilities
- Maintain account security
- Comply with applicable laws
- Obtain consent before recording calls

## 4. Data Processing
You consent to data processing as described in our Privacy Policy.

## 5. Termination
You may terminate your account at any time.

## 6. Limitation of Liability
Service is provided "as is" without warranties.

Last updated: """ + datetime.utcnow().strftime('%Y-%m-%d')
    }
