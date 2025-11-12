from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import json

from app.models.agent import Agent
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.call_log import CallLog
from app.services.llm_service import llm_service
from app.services.elevenlabs_service import elevenlabs_service
from app.services.tool_executor import ToolExecutor


class ConversationManager:
    """Manage conversation flow between user and AI agent"""

    def __init__(
        self,
        agent: Agent,
        db: AsyncSession,
        conversation: Optional[Conversation] = None,
        call_sid: Optional[str] = None
    ):
        self.agent = agent
        self.db = db
        self.conversation = conversation
        self.call_sid = call_sid
        self.messages: List[Dict[str, str]] = []
        self.tool_executor = ToolExecutor(agent.tools_config, call_sid)

        # Initialize with system prompt
        self.messages.append({
            "role": "system",
            "content": agent.system_prompt
        })

    async def process_message(self, user_input: str, save_to_db: bool = False) -> str:
        """
        Process a user message and return agent's response

        Args:
            user_input: The user's message
            save_to_db: Whether to save messages to database

        Returns:
            Agent's response text
        """
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        # Save user message to DB if requested
        if save_to_db and self.conversation:
            user_message = Message(
                conversation_id=self.conversation.id,
                role="user",
                content=user_input,
                timestamp=datetime.utcnow()
            )
            self.db.add(user_message)
            await self.db.commit()

        # Get tool definitions for LLM
        tools = self.tool_executor.get_tool_definitions_for_llm()

        # Get LLM response
        response_text = ""
        tool_calls = []

        async for chunk in llm_service.chat_completion(
            messages=self.messages,
            tools=tools if tools else None,
            stream=True
        ):
            # Check if it's a tool call
            try:
                chunk_data = json.loads(chunk)
                if "tool_call" in chunk_data:
                    tool_calls.append(chunk_data["tool_call"])
                    continue
            except (json.JSONDecodeError, TypeError):
                pass

            # Regular text response
            response_text += chunk

        # Handle tool calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = json.loads(tool_call["arguments"]) if isinstance(tool_call["arguments"], str) else tool_call["arguments"]

                # Execute tool
                tool_result = await self.tool_executor.execute_tool(tool_name, tool_args)

                # Add tool result to conversation
                self.messages.append({
                    "role": "function",
                    "name": tool_name,
                    "content": tool_result
                })

                # Get another LLM response incorporating tool result
                follow_up_response = ""
                async for chunk in llm_service.chat_completion(
                    messages=self.messages,
                    stream=True
                ):
                    follow_up_response += chunk

                response_text += " " + follow_up_response

        # Add assistant response to history
        self.messages.append({
            "role": "assistant",
            "content": response_text
        })

        # Save assistant message to DB if requested
        if save_to_db and self.conversation:
            assistant_message = Message(
                conversation_id=self.conversation.id,
                role="assistant",
                content=response_text,
                timestamp=datetime.utcnow()
            )
            self.db.add(assistant_message)
            await self.db.commit()

        return response_text.strip()

    async def get_speech_response(self, user_input: str) -> bytes:
        """
        Process message and return audio response

        Args:
            user_input: The user's message

        Returns:
            Audio bytes from TTS
        """
        # Get text response
        text_response = await self.process_message(user_input, save_to_db=True)

        # Convert to speech
        audio = await elevenlabs_service.text_to_speech(
            text=text_response,
            voice_id=self.agent.voice_id
        )

        return audio

    async def end_conversation(self) -> None:
        """End the conversation and create call log"""
        if not self.conversation:
            return

        # Update conversation end time
        self.conversation.end_time = datetime.utcnow()
        self.conversation.status = "completed"

        # Calculate duration
        duration = (self.conversation.end_time - self.conversation.start_time).total_seconds()

        # Create transcript
        transcript_lines = []
        for msg in self.messages[1:]:  # Skip system message
            role = msg["role"]
            content = msg["content"]
            if role in ["user", "assistant"]:
                transcript_lines.append(f"{role.upper()}: {content}")

        transcript = "\n".join(transcript_lines)

        # Generate summary
        summary = await llm_service.create_conversation_summary(self.messages[1:])

        # Create call log
        call_log = CallLog(
            conversation_id=self.conversation.id,
            duration=duration,
            status="completed",
            transcript=transcript,
            summary=summary
        )

        self.db.add(call_log)
        await self.db.commit()
