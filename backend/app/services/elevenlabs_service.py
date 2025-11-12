from elevenlabs import generate
from app.core.config import settings
from typing import Optional


class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel

    async def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model: str = "eleven_turbo_v2_5"  # Fast model for real-time
    ) -> bytes:
        """
        Convert text to speech using ElevenLabs

        For the fastest latency, use:
        - Model: eleven_turbo_v2_5 (or eleven_turbo_v2 for conversational AI)
        - This provides ~150ms latency as mentioned
        """
        voice_id = voice_id or self.default_voice_id

        # Generate audio
        audio = generate(
            text=text,
            voice=voice_id,
            model=model,
            api_key=self.api_key
        )

        # Convert generator to bytes
        audio_bytes = b"".join(audio)
        return audio_bytes

    async def text_to_speech_stream(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model: str = "eleven_turbo_v2_5"
    ):
        """
        Stream text to speech for lower latency
        Returns an async generator of audio chunks
        """
        voice_id = voice_id or self.default_voice_id

        # Use streaming for real-time response
        audio_stream = generate(
            text=text,
            voice=voice_id,
            model=model,
            stream=True,
            api_key=self.api_key
        )

        return audio_stream

    async def get_voices(self):
        """Get available voices from ElevenLabs"""
        # Return default voices
        return {
            "voices": [
                {"voice_id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel"},
                {"voice_id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi"},
                {"voice_id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella"},
                {"voice_id": "ErXwobaYiN019PkySvjV", "name": "Antoni"},
            ]
        }


# Singleton instance
elevenlabs_service = ElevenLabsService()
