"""
Background worker for scheduled tasks
Handles data retention, anonymization, and cleanup
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.call_log import CallLog
from app.models.message import Message
from app.models.conversation import Conversation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def cleanup_old_recordings():
    """Delete recordings past retention period"""
    logger.info("Running cleanup of old recordings...")

    async with AsyncSessionLocal() as db:
        # Find call logs past retention
        cutoff_date = datetime.utcnow()

        result = await db.execute(
            select(CallLog).where(CallLog.retention_until < cutoff_date)
        )
        old_logs = result.scalars().all()

        deleted_count = 0
        for log in old_logs:
            # Delete audio files (implement file deletion logic)
            # For now, just clear the transcript
            log.transcript = "[DELETED - Retention period expired]"
            deleted_count += 1

        await db.commit()
        logger.info(f"Cleaned up {deleted_count} old call logs")


async def anonymize_old_messages():
    """Anonymize messages past anonymization period"""
    logger.info("Running anonymization of old messages...")

    async with AsyncSessionLocal() as db:
        # Find conversations past anonymization period
        cutoff_date = datetime.utcnow() - timedelta(days=settings.ANONYMIZATION_AFTER_DAYS)

        result = await db.execute(
            select(Conversation).where(
                Conversation.end_time < cutoff_date,
                Conversation.end_time.isnot(None)
            )
        )
        old_conversations = result.scalars().all()

        anonymized_count = 0
        for conversation in old_conversations:
            # Anonymize messages
            messages_result = await db.execute(
                select(Message).where(
                    Message.conversation_id == conversation.id,
                    Message.anonymized == False
                )
            )
            messages = messages_result.scalars().all()

            for message in messages:
                # Simple anonymization - hash the content
                message.content = f"[ANONYMIZED_{message.id}]"
                message.anonymized = True
                anonymized_count += 1

        await db.commit()
        logger.info(f"Anonymized {anonymized_count} messages")


async def process_deletion_requests():
    """Process pending data deletion requests"""
    logger.info("Processing deletion requests...")

    from app.models.data_deletion_request import DataDeletionRequest
    from app.models.user import User

    async with AsyncSessionLocal() as db:
        # Find pending deletion requests
        result = await db.execute(
            select(DataDeletionRequest).where(
                DataDeletionRequest.status == "pending"
            )
        )
        requests = result.scalars().all()

        for request in requests:
            try:
                # Get user
                user_result = await db.execute(
                    select(User).where(User.id == request.user_id)
                )
                user = user_result.scalar_one_or_none()

                if user:
                    # Delete user (cascade will handle related data)
                    await db.delete(user)

                    # Mark request as completed
                    request.status = "completed"
                    request.completed_at = datetime.utcnow()

                    await db.commit()
                    logger.info(f"Deleted user {user.email} (request {request.id})")
                else:
                    # User already deleted
                    request.status = "completed"
                    request.completed_at = datetime.utcnow()
                    await db.commit()

            except Exception as e:
                logger.error(f"Failed to process deletion request {request.id}: {str(e)}")
                request.status = "failed"
                request.notes = str(e)
                await db.commit()


async def run_scheduled_tasks():
    """Run all scheduled tasks in a loop"""
    logger.info("Worker started")

    while True:
        try:
            # Run cleanup tasks
            await cleanup_old_recordings()
            await anonymize_old_messages()
            await process_deletion_requests()

            # Sleep for 1 hour
            logger.info("Sleeping for 1 hour...")
            await asyncio.sleep(3600)

        except Exception as e:
            logger.error(f"Error in scheduled tasks: {str(e)}")
            await asyncio.sleep(300)  # Sleep 5 minutes on error


if __name__ == "__main__":
    asyncio.run(run_scheduled_tasks())
