from fastapi import APIRouter, WebSocket, Request, Response
from fastapi.websockets import WebSocketDisconnect
from app.services.audio_orchestrator import AudioOrchestrator
from app.utils import logger
import os

router = APIRouter()

@router.api_route("/incoming", methods=["GET", "POST"])
async def incoming_call(request: Request):
    """
    Handle incoming calls from Twilio.
    Returns TwiML to connect to the Media Stream.
    """
    if request.method == "GET":
        return Response(content="Twilio Webhook Ready. Please configure Twilio to use POST.", media_type="text/plain")

    # Get the host from the request or environment
    # In production (Render), we might need to rely on the Host header or a configured URL
    host = request.headers.get("host")
    
    # Construct the WebSocket URL
    # If standard http/https, ws uses ws/wss
    # Twilio requires wss for secure connections (which keys usually imply)
    # properly handled by Twilio but let's be explicit if needed.
    # Actually, simplest is to just use the host.
    
    ws_url = f"wss://{host}/voice/stream"
    
    logger.info(f"Incoming call. Redirecting to Media Stream at {ws_url}")

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>
"""
    return Response(content=twiml_response, media_type="application/xml")


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for Twilio Media Streams.
    """
    orchestrator = AudioOrchestrator(websocket)
    await orchestrator.start()
