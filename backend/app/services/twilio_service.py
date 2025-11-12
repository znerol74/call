from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from app.core.config import settings
from typing import Optional


class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.phone_number = settings.TWILIO_PHONE_NUMBER

    def create_call(self, to_number: str, callback_url: str) -> str:
        """Initiate an outbound call"""
        call = self.client.calls.create(
            to=to_number,
            from_=self.phone_number,
            url=callback_url,
            method='POST'
        )
        return call.sid

    def transfer_call(self, call_sid: str, to_number: str) -> None:
        """Transfer an active call to another number"""
        call = self.client.calls(call_sid).update(
            twiml=f'<Response><Dial>{to_number}</Dial></Response>'
        )

    def end_call(self, call_sid: str) -> None:
        """End an active call"""
        self.client.calls(call_sid).update(status='completed')

    def create_twiml_response(self, message: str, gather: bool = True) -> str:
        """Create TwiML response for Twilio webhook"""
        response = VoiceResponse()

        if gather:
            # Gather speech input
            gather_obj = Gather(
                input='speech',
                action='/api/v1/twilio/process-speech',
                method='POST',
                language='de-DE',
                speech_timeout='auto',
                timeout=5
            )
            gather_obj.say(message, language='de-DE')
            response.append(gather_obj)
        else:
            response.say(message, language='de-DE')

        return str(response)

    def create_stream_response(self, websocket_url: str) -> str:
        """Create TwiML response with media stream for real-time audio"""
        response = VoiceResponse()
        response.say("Verbinde...")

        # Start media stream
        start = response.start()
        stream = start.stream(
            url=websocket_url,
            track='both_tracks'
        )

        # Keep call alive
        response.pause(length=60)

        return str(response)


# Singleton instance
twilio_service = TwilioService()
