from openai import AsyncAzureOpenAI
from app.core.config import settings
from typing import List, Dict, Any, Optional, AsyncGenerator
import json


class LLMService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> AsyncGenerator[str, None]:
        """
        Get chat completion from Azure OpenAI with streaming

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
            stream: Whether to stream the response
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Yields:
            Response chunks as they arrive (if streaming)
        """
        kwargs = {
            "model": self.deployment,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        # Add tools if provided
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(**kwargs)

        if stream:
            # Stream response chunks
            async for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta

                    # Check for content
                    if delta.content:
                        yield delta.content

                    # Check for tool calls
                    if delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            if tool_call.function:
                                yield json.dumps({
                                    "tool_call": {
                                        "name": tool_call.function.name,
                                        "arguments": tool_call.function.arguments
                                    }
                                })
        else:
            # Non-streaming response
            if response.choices and len(response.choices) > 0:
                message = response.choices[0].message

                if message.content:
                    yield message.content

                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        yield json.dumps({
                            "tool_call": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        })

    async def create_conversation_summary(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Create a summary of a conversation"""
        summary_prompt = [
            {
                "role": "system",
                "content": "Fasse das folgende Gespräch in 2-3 Sätzen zusammen. Konzentriere dich auf die wichtigsten Punkte und Ergebnisse."
            },
            {
                "role": "user",
                "content": f"Gespräch:\n{json.dumps(messages, ensure_ascii=False, indent=2)}"
            }
        ]

        summary = ""
        async for chunk in self.chat_completion(summary_prompt, stream=True):
            summary += chunk

        return summary.strip()


# Singleton instance
llm_service = LLMService()
