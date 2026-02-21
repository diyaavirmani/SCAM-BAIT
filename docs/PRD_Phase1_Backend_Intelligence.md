# 📄 PRD: Phase 1 - Core Backend & Intelligence (Member 1)

**Role:** Backend Lead
**Focus:** API, Core Logic, Database, Intelligence Extraction
**Branch Name:** `feature/backend-intelligence`

---

## 🎯 Objective
Enhance the existing FastAPI backend to support real-time dashboard data and improve scam detection intelligence. You are the foundation of the project.

## 🛠️ Tech Stack & Tools
-   **Language:** Python 3.11+
-   **Framework:** FastAPI (Async)
-   **Database:** SQLite (Current) -> Prepared for PostgreSQL migration if needed
-   **AI/ML:** LangChain, Regex, Scikit-learn
-   **Real-time:** WebSockets (FastAPI native)

## 🚫 Critical Rules (Simulated Environment)
> **[IMPORTANT]**
> *   **DO NOT run commands yourself.** You are in a simulated coding environment.
> *   Your job is to write code and define logic. We will handle the execution.
> *   **ALWAYS** work on your specific branch: `feature/backend-intelligence`.
> *   **NEVER** touch frontend or voice files.

---

## 📋 Features to Build

### 1. **Real-Time WebSocket Endpoint**
**Goal:** Stream live data to the dashboard.
*   **Action:** Create a new WebSocket endpoint `/ws/dashboard`.
*   **Logic:**
    *   Accept connections from the frontend.
    *   Broadcast `session_update` events whenever a new message is received or sent.
    *   Broadcast `intelligence_update` events when new data (phone, UPI) is extracted.
    *   Maintain a list of active websocket connections.

### 2. **Enhanced Intelligence Extraction**
**Goal:** Capture more data points from scammers.
*   **Action:** Update `app/agents/extraction.py`.
*   **New Regex Patterns to Add:**
    *   **Email Addresses:** `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
    *   **APK Links:** `http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.apk`
    *   **Crypto Wallets:** (Bitcoin, Ethereum, TRON addresses)
    *   **Social Handles:** `@username` (Telegram/Twitter)
    *   **Bank IFSC:** `^[A-Z]{4}0[A-Z0-9]{6}$`

### 3. **Scam Type Classification**
**Goal:** Categorize the scam automatically.
*   **Action:** Modify `app/agents/detection.py`.
*   **Logic:**
    *   Analyze message content against keyword sets.
    *   **Categories:**
        *   `DIGITAL_ARREST` (Keywords: CBI, police, arrest, drugs, fedex)
        *   `UPI_SCAM` (Keywords: cashback, refund, pin, qr code)
        *   `JOB_SCAM` (Keywords: part time, work from home, daily income)
        *   `SEXTORTION` (Keywords: video call, recording, viral)
    *   Add `scam_type` field to the session metadata.

### 4. **Session Analytics API**
**Goal:** Provide stats for the dashboard.
*   **Action:** Create API endpoint `/api/v1/stats`.
*   **Return Data:**
    *   `total_sessions`: Count of all interactions.
    *   `scams_detected`: Count of confirmed scams.
    *   `intelligence_items`: Count of phone numbers/UPIs extracted.
    *   `active_now`: Number of currently active sessions.

---

## 🗓️ Step-by-Step Implementation Guide

**Step 1: Create Branch**
*   (We will run: `git checkout -b feature/backend-intelligence`)

**Step 2: Define Data Models**
*   Update `app/models.py` to include `ScamType` enum and `IntelligenceData` extended fields (email, apk, etc.).

**Step 3: Implement WebSockets**
*   Create `app/websockets.py`.
*   Implement `ConnectionManager` class to handle connect/disconnect/broadcast.
*   Integrate into `app/main.py`.

**Step 4: Upgrade Extraction Agent**
*   Add the new regex patterns to `app/agents/extraction.py`.
*   Test with sample scam messages containing APK links and emails.

**Step 5: Implement Stats API**
*   Create the `/stats` endpoint in `app/main.py`.
*   Write a query to aggregate data from the SQLite database.

## 🧪 Testing
*   Use `Postman` or `curl` to test HTTP endpoints.
*   Use a WebSocket client (like `wscat` or Postman) to test `/ws/dashboard`.
