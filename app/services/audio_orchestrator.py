import os
import json
import base64
import asyncio
import logging
import websockets
from fastapi import WebSocket, WebSocketDisconnect
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from elevenlabs.client import ElevenLabs
from app.utils import logger
from app.agents.persona import generate_persona_response

class AudioOrchestrator:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.deepgram_client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Default voice if not set
        self.stream_sid = None
        self.deepgram_connection = None
        self.is_listening = False
        self.conversation_history = [] # List of {"sender": "scammer" | "ai", "text": "..."}

    async def start(self):
        """Initialize connections to Deepgram and start processing."""
        await self.websocket.accept()
        
        # Initialize Deepgram Live Client
        # Note: Using v("1") as per SDK examples, ensuring options are correct
        self.deepgram_connection = self.deepgram_client.listen.live.v("1")
        
        # Register Deepgram Event Handlers
        self.deepgram_connection.on(LiveTranscriptionEvents.Transcript, self.on_transcript)
        self.deepgram_connection.on(LiveTranscriptionEvents.Error, self.on_error)
        
        # Configure Deepgram Options
        options = LiveOptions(
            model="nova-2",
            language="en-US", # Can be multi-language in future
            smart_format=True,
            encoding="mulaw",
            sample_rate=8000,
            channels=1,
            interim_results=False, # We only want final results for now
            vad_events=True, # Voice Activity Detection
            endpointing=500, # Wait 500ms of silence
        )

        # Start Deepgram Connection
        if not self.deepgram_connection.start(options):
            logger.error("Failed to start Deepgram connection")
            await self.websocket.close()
            return

        logger.info("Deepgram connection started")
        self.is_listening = True
        
        try:
            while True:
                # Twilio sends JSON messages over the WebSocket
                message = await self.websocket.receive_text()
                data = json.loads(message)
                await self.handle_twilio_message(data)
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"Error in AudioOrchestrator loop: {e}")
        finally:
            await self.cleanup()

    async def handle_twilio_message(self, data):
        """Handle incoming messages from Twilio via WebSocket."""
        event = data.get("event")

        if event == "start":
            self.stream_sid = data["start"]["streamSid"]
            logger.info(f"Twilio Stream started: {self.stream_sid}")

            # Initial greeting with ElevenLabs voice
            initial_text = "Hello? Who is this?"
            self.conversation_history.append({"sender": "ai", "text": initial_text})
            asyncio.create_task(self.stream_tts(initial_text))
        
        elif event == "media":
            if self.is_listening and self.deepgram_connection:
                payload = data["media"]["payload"]
                audio_data = base64.b64decode(payload)
                self.deepgram_connection.send(audio_data)
        
        elif event == "stop":
            logger.info("Twilio Stream stopped")
            await self.cleanup()

    def on_transcript(self, sender, result, **kwargs):
        """Handle transcript received from Deepgram."""
        if not result:
            return

        if not result.channel.alternatives:
            return
            
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return
            
        if result.is_final:
            logger.info(f"User said: {sentence}")
            # Update history
            self.conversation_history.append({"sender": "scammer", "text": sentence})
            
            # Process the text with LLM and generate response asynchronously
            # Since this callback runs in a separate thread, we need to schedule it on the main loop
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.process_response(sentence))
            except RuntimeError:
                # If no running loop in this thread, find the main loop or create a new task safely
                # But typically we should have a reference to the main loop.
                # Let's assume the loop where __init__ or start() was called is the main loop.
                # Better approach: store the loop in __init__
                pass

    def on_error(self, sender, error, **kwargs):
        logger.error(f"Deepgram error: {error} | Sender: {sender} | Kwargs: {kwargs}")

    async def process_response(self, text):
        """Send text to LLM and stream audio back to Twilio."""
        try:
            # 1. Get LLM Response
            metadata = {
                "source": "voice_call",
                "phone_number": "unknown",
                "language": "English"
            }

            response_text = await generate_persona_response(
                conversation_history=self.conversation_history,
                metadata=metadata
            )
            
            logger.info(f"AI Response: {response_text}")
            self.conversation_history.append({"sender": "ai", "text": response_text})

            # 2. Text-to-Speech (ElevenLabs)
            await self.stream_tts(response_text)
            
        except Exception as e:
            logger.error(f"Error in process_response: {e}")

    async def stream_tts(self, text):
        """Stream audio from ElevenLabs to Twilio."""
        try:
            # Generate audio stream from ElevenLabs (v1+ SDK)
            audio_stream = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_turbo_v2",
                output_format="ulaw_8000"
            )

            for chunk in audio_stream:
                if chunk:
                    # Encode to base64 for Twilio
                    audio_payload = base64.b64encode(chunk).decode("utf-8")
                    media_message = {
                        "event": "media",
                        "streamSid": self.stream_sid,
                        "media": {
                            "payload": audio_payload
                        }
                    }
                    await self.websocket.send_json(media_message)
            
            # Send a mark event? Not strictly necessary unless we want to handle interruptions perfectly.
            
        except Exception as e:
            logger.error(f"Error streaming TTS: {e}")

    async def cleanup(self):
        """Close connections and clean up resources."""
        self.is_listening = False
        if self.deepgram_connection:
            self.deepgram_connection.finish()
        logger.info("AudioOrchestrator cleaned up")
