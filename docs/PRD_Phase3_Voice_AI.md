# 📄 PRD: Phase 3 - Voice AI & Advanced Features (Member 3)

**Role:** Voice AI Lead
**Focus:** Telephony, Speech-to-Text (STT), Text-to-Speech (TTS)
**Branch Name:** `feature/voice-ai`

---

## 🎯 Objective
Enable the Honeypot to handle **voice calls**. Scammers calling the "victim" number should hear a convincing elderly AI that responds in real-time, transcribing the call for the dashboard.

## 🛠️ Tech Stack & Tools
-   **Telephony:** Twilio (Programmable Voice)
-   **STT (Ear):** Deepgram (Nova-2 Model for speed)
-   **TTS (Mouth):** ElevenLabs (Turbo v2.5 for low latency)
-   **Orchestration:** Python (FastAPI + Twilio Media Streams)
-   **Local Testing:** PyAudio / ngrok

## 🚫 Critical Rules (Simulated Environment)
> **[IMPORTANT]**
> *   **DO NOT run commands yourself.** You are in a simulated coding environment.
> *   **ALWAYS** work on your specific branch: `feature/voice-ai`.
> *   **NEVER** touch the dashboard or core database logic.

---

## 📋 Features to Build

### 1. **Twilio Media Stream Handler**
**Goal:** Receive raw audio from a phone call.
*   **Action:** Create API endpoint `/voice/stream`.
*   **Logic:**
    *   Accept WebSocket connection from Twilio.
    *   Receive audio payload (base64).
    *   Forward audio to Deepgram.

### 2. **Deepgram Transcription Integration**
**Goal:** Convert scammer speech to text instantly.
*   **Action:** Update `app/agents/voice.py`.
*   **Logic:**
    *   Stream audio to Deepgram API.
    *   Receive `is_final=true` transcripts.
    *   Send transcript to the **Core Backend** (Member 1's logic) to generate a text response.

### 3. **ElevenLabs Response Generation**
**Goal:** Convert AI text response to "Elderly Voice" audio.
*   **Action:** Update `app/agents/voice.py`.
*   **Logic:**
    *   Take text response from LLM.
    *   Send to ElevenLabs API (use `ElevenLabs Turbo` model).
    *   Stream audio back to Twilio via WebSocket.

### 4. **Voice Scenario Logic**
**Goal:** Handle silence and interruptions.
*   **Action:** Implement "Barge-in" logic.
*   **Logic:**
    *   If scammer speaks while AI is talking -> Stop AI audio (Clear buffer).
    *   If silence > 5 seconds -> AI says "Hello? Are you there?"

---

## 🗓️ Step-by-Step Implementation Guide

**Step 1: Create Branch**
*   (We will run: `git checkout -b feature/voice-ai`)

**Step 2: Setup Twilio Webhook Logic**
*   Create `app/voice_router.py`.
*   Define the TwiML response to `<Connect><Stream url="..." /></Connect>`.

**Step 3: Build the Audio Pipeline Class**
*   Create `app/services/audio_orchestrator.py`.
*   Methods: `process_incoming_audio()`, `synthesize_and_send()`.

**Step 4: Integrate ElevenLabs**
*   Add `ELEVENLABS_API_KEY` to config.
*   Select a specific Voice ID (e.g., "Fin" or "Nicole" - elderly variants).

**Step 5: Integration Test**
*   Since we can't make real calls easily in dev without ngrok:
*   Create a local script `tests/simulate_call.py` that uses your microphone as input and plays back the AI response on speakers.

## 🧪 Testing
*   **Local:** Run `python tests/simulate_call.py` -> Speak into mic -> Hear AI response.
*   **Production:** Deploy key components and call the Twilio number.
