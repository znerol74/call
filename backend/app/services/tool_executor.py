import httpx
import json
from typing import Dict, Any, List
from app.services.twilio_service import twilio_service


class ToolExecutor:
    """Execute tools defined by agents"""

    def __init__(self, tools_config: List[Dict[str, Any]], call_sid: str = None):
        self.tools_config = tools_config or []
        self.call_sid = call_sid

    def get_tool_definitions_for_llm(self) -> List[Dict[str, Any]]:
        """
        Convert agent's tool config to OpenAI function calling format
        """
        if not self.tools_config:
            return []

        llm_tools = []
        for tool in self.tools_config:
            llm_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })

        return llm_tools

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a tool and return the result

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool

        Returns:
            String result of tool execution
        """
        # Find tool in config
        tool_config = None
        for tool in self.tools_config:
            if tool["name"] == tool_name:
                tool_config = tool
                break

        if not tool_config:
            return f"Error: Tool '{tool_name}' not found"

        # Execute based on tool name
        if tool_name == "transfer_call":
            return await self._transfer_call(arguments)
        elif tool_name == "end_call":
            return await self._end_call()
        elif tool_name == "api_call":
            return await self._api_call(arguments)
        elif tool_name == "get_weather":
            return await self._get_weather(arguments)
        else:
            return f"Error: Tool '{tool_name}' execution not implemented"

    async def _transfer_call(self, arguments: Dict[str, Any]) -> str:
        """Transfer the call to another number"""
        phone_number = arguments.get("phone_number")

        if not phone_number:
            return "Error: phone_number required"

        if not self.call_sid:
            return "Error: No active call to transfer"

        try:
            twilio_service.transfer_call(self.call_sid, phone_number)
            return f"Call transferred to {phone_number}"
        except Exception as e:
            return f"Error transferring call: {str(e)}"

    async def _end_call(self) -> str:
        """End the current call"""
        if not self.call_sid:
            return "Error: No active call"

        try:
            twilio_service.end_call(self.call_sid)
            return "Call ended"
        except Exception as e:
            return f"Error ending call: {str(e)}"

    async def _api_call(self, arguments: Dict[str, Any]) -> str:
        """Make an HTTP API call"""
        url = arguments.get("url")
        method = arguments.get("method", "GET").upper()
        headers = arguments.get("headers", {})
        body = arguments.get("body")

        if not url:
            return "Error: url required"

        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, headers=headers, json=body)
                elif method == "PUT":
                    response = await client.put(url, headers=headers, json=body)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    return f"Error: Unsupported HTTP method {method}"

                return f"API call successful. Status: {response.status_code}. Response: {response.text[:200]}"
        except Exception as e:
            return f"Error making API call: {str(e)}"

    async def _get_weather(self, arguments: Dict[str, Any]) -> str:
        """Get weather for a location (example tool)"""
        location = arguments.get("location")

        if not location:
            return "Error: location required"

        # This is a mock implementation
        # In production, you'd call a real weather API
        return f"Das Wetter in {location} ist sonnig mit 22°C."
