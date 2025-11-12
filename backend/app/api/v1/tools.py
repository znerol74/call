from fastapi import APIRouter

router = APIRouter()


@router.get("/available-tools")
async def get_available_tools():
    """Get list of available tool types that can be configured for agents"""
    return {
        "tools": [
            {
                "name": "transfer_call",
                "description": "Transfer the call to another phone number",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "The phone number to transfer to"
                        }
                    },
                    "required": ["phone_number"]
                }
            },
            {
                "name": "end_call",
                "description": "End the current call",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "api_call",
                "description": "Make an HTTP API call",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to call"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["GET", "POST", "PUT", "DELETE"],
                            "description": "HTTP method"
                        },
                        "headers": {
                            "type": "object",
                            "description": "HTTP headers"
                        },
                        "body": {
                            "type": "object",
                            "description": "Request body for POST/PUT"
                        }
                    },
                    "required": ["url", "method"]
                }
            },
            {
                "name": "get_weather",
                "description": "Get current weather for a location (example tool)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name or location"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
    }
