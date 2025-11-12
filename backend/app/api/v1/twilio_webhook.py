from fastapi import APIRouter, Form, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.database import AsyncSessionLocal
from app.models.phone_number import PhoneNumber
from app.models.agent import Agent
from app.models.conversation import Conversation
from app.services.twilio_service import twilio_service
from app.services.conversation_manager import ConversationManager

router = APIRouter()

# Store active conversations
active_conversations = {}


@router.post("/incoming-call")
async def handle_incoming_call(
    From: str = Form(...),
    To: str = Form(...),
    CallSid: str = Form(...)
):
    """Handle incoming Twilio call"""
    async with AsyncSessionLocal() as db:
        # Find phone number and associated agent
        result = await db.execute(
            select(PhoneNumber).where(PhoneNumber.phone_number == To)
        )
        phone_number_record = result.scalar_one_or_none()

        if not phone_number_record or not phone_number_record.agent_id:
            # No agent configured for this number
            twiml = twilio_service.create_twiml_response(
                "Entschuldigung, kein Agent ist für diese Nummer konfiguriert.",
                gather=False
            )
            return Response(content=twiml, media_type="application/xml")

        # Get agent
        agent_result = await db.execute(
            select(Agent).where(Agent.id == phone_number_record.agent_id)
        )
        agent = agent_result.scalar_one_or_none()

        if not agent:
            twiml = twilio_service.create_twiml_response(
                "Entschuldigung, der Agent konnte nicht gefunden werden.",
                gather=False
            )
            return Response(content=twiml, media_type="application/xml")

        # Create conversation
        conversation = Conversation(
            user_id=agent.user_id,
            agent_id=agent.id,
            phone_number_id=phone_number_record.id,
            caller_phone_number=From,
            call_sid=CallSid,
            direction="inbound",
            status="active"
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

        # Create conversation manager
        conv_manager = ConversationManager(
            agent=agent,
            db=db,
            conversation=conversation,
            call_sid=CallSid
        )
        active_conversations[CallSid] = conv_manager

        # Respond with greeting
        twiml = twilio_service.create_twiml_response(agent.greeting_message, gather=True)
        return Response(content=twiml, media_type="application/xml")


@router.post("/process-speech")
async def process_speech(
    SpeechResult: str = Form(None),
    CallSid: str = Form(...),
    UnstableSpeechResult: str = Form(None)
):
    """Process speech input from Twilio"""
    user_input = SpeechResult or UnstableSpeechResult

    if not user_input:
        twiml = twilio_service.create_twiml_response(
            "Entschuldigung, ich habe Sie nicht verstanden. Können Sie das wiederholen?",
            gather=True
        )
        return Response(content=twiml, media_type="application/xml")

    # Get conversation manager
    conv_manager = active_conversations.get(CallSid)

    if not conv_manager:
        twiml = twilio_service.create_twiml_response(
            "Entschuldigung, es gab ein technisches Problem.",
            gather=False
        )
        return Response(content=twiml, media_type="application/xml")

    # Process message
    response_text = await conv_manager.process_message(user_input, save_to_db=True)

    # Create TwiML response
    twiml = twilio_service.create_twiml_response(response_text, gather=True)
    return Response(content=twiml, media_type="application/xml")


@router.post("/call-status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...)
):
    """Handle call status updates"""
    if CallStatus in ["completed", "failed", "busy", "no-answer"]:
        # End conversation
        conv_manager = active_conversations.get(CallSid)

        if conv_manager:
            await conv_manager.end_conversation()
            del active_conversations[CallSid]

    return {"status": "ok"}
