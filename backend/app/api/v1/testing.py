from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict
import json

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.agent import Agent
from app.services.conversation_manager import ConversationManager

router = APIRouter()

# Store active test sessions
active_sessions: Dict[str, ConversationManager] = {}


@router.websocket("/ws/{agent_id}")
async def websocket_test_agent(
    websocket: WebSocket,
    agent_id: int,
):
    """WebSocket endpoint for testing agents in real-time"""
    await websocket.accept()

    try:
        # Authenticate via first message (expecting {"token": "..."})
        auth_message = await websocket.receive_text()
        auth_data = json.loads(auth_message)
        token = auth_data.get("token")

        if not token:
            await websocket.send_json({"error": "Authentication required"})
            await websocket.close()
            return

        # Verify token
        try:
            payload = decode_token(token, "access")
            user_id = payload.get("sub")
        except:
            await websocket.send_json({"error": "Invalid token"})
            await websocket.close()
            return

        # Get database session
        async for db in get_db():
            # Verify agent belongs to user
            result = await db.execute(
                select(Agent).where(Agent.id == agent_id, Agent.user_id == user_id)
            )
            agent = result.scalar_one_or_none()

            if not agent:
                await websocket.send_json({"error": "Agent not found"})
                await websocket.close()
                return

            # Send greeting
            await websocket.send_json({
                "type": "greeting",
                "content": agent.greeting_message
            })

            # Create conversation manager
            session_id = f"test_{user_id}_{agent_id}"
            conversation_manager = ConversationManager(agent, db)
            active_sessions[session_id] = conversation_manager

            # Handle messages
            try:
                while True:
                    # Receive user message
                    message = await websocket.receive_text()
                    message_data = json.loads(message)

                    if message_data.get("type") == "text":
                        user_input = message_data.get("content")

                        # Process with agent
                        response = await conversation_manager.process_message(user_input)

                        # Send response
                        await websocket.send_json({
                            "type": "text",
                            "content": response
                        })

                    elif message_data.get("type") == "audio":
                        # Handle audio input (future feature)
                        await websocket.send_json({
                            "type": "error",
                            "content": "Audio input not yet implemented"
                        })

            except WebSocketDisconnect:
                # Clean up session
                if session_id in active_sessions:
                    del active_sessions[session_id]
                break

            break  # Exit db session loop

    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


@router.get("/voices")
async def get_available_voices():
    """Get list of available ElevenLabs voices"""
    # This would normally call ElevenLabs API
    # For now, return some example voices
    return {
        "voices": [
            {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "name": "Rachel",
                "gender": "female",
                "language": "en"
            },
            {
                "voice_id": "AZnzlk1XvdvUeBnXmlld",
                "name": "Domi",
                "gender": "female",
                "language": "en"
            },
            {
                "voice_id": "EXAVITQu4vr4xnSDxMaL",
                "name": "Bella",
                "gender": "female",
                "language": "en"
            },
            {
                "voice_id": "ErXwobaYiN019PkySvjV",
                "name": "Antoni",
                "gender": "male",
                "language": "en"
            },
            {
                "voice_id": "VR6AewLTigWG4xSOukaG",
                "name": "Arnold",
                "gender": "male",
                "language": "en"
            },
        ]
    }
