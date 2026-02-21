# 📄 PRD: Phase 2 - Real-time Dashboard (Member 2)

**Role:** Frontend Lead
**Focus:** Dashboard UI, Data Visualization, WebSocket Integration
**Branch Name:** `feature/frontend-dashboard`

---

## 🎯 Objective
Build a professional, hacker-style real-time dashboard that visualizes active scams, displays extracted intelligence live, and impresses judges with "movie-like" aesthetics.

## 🛠️ Tech Stack & Tools
-   **Framework:** React (via Vite)
-   **Language:** TypeScript
-   **Styling:** TailwindCSS + ShadcnUI (for professional components)
-   **Charts:** Recharts (Best for live data)
-   **Icons:** Lucide-React
-   **State Management:** React Context + Hooks

## 🚫 Critical Rules (Simulated Environment)
> **[IMPORTANT]**
> *   **DO NOT run commands yourself.** You are in a simulated coding environment.
> *   **ALWAYS** work on your specific branch: `feature/frontend-dashboard`.
> *   **NEVER** touch backend logic or PyAudio files.

---

## 📋 Features to Build

### 1. **Live Session Monitor**
**Goal:** Show active chats scrolling in real-time (Matrix style).
*   **Component:** `LiveFeed.tsx`
*   **Logic:**
    *   Connect to WebSocket `/ws/dashboard`.
    *   Display incoming messages with timestamp and sender (Scammer/AI).
    *   Auto-scroll to bottom.

### 2. **Intelligence Widget**
**Goal:** "Pop up" extracted data cards when found.
*   **Component:** `IntelligenceCard.tsx`
*   **Logic:**
    *   Listen for `intelligence_update` events.
    *   When phone/UPI is found, trigger a rigid animation (red border flash).
    *   Display details: `Type: PHONE`, `Value: +91-98...`, `Confidence: HIGH`.

### 3. **Global Analytics Headers**
**Goal:** High-level metrics at the top.
*   **Component:** `StatCards.tsx`
*   **Metrics:**
    *   `Active Scams` (Live count)
    *   `Money Saved` (Estimated ₹₹₹)
    *   `Scammers Exposed` (Total unique phones)

### 4. **Network Graph (Bonus)**
**Goal:** Visual connection map.
*   **Component:** `ScamNetwork.tsx`
*   **Library:** `react-force-graph` or simple SVG lines.
*   **Display:** Nodes = Phone Numbers/UPIs. Edges = Shared Sessions.

---

## 🗓️ Step-by-Step Implementation Guide

**Step 1: Initialize Project**
*   (We will run: `npm create vite@latest dashboard -- --template react-ts`)
*   (We will run: `npm install -D tailwindcss postcss autoprefixer`)

**Step 2: Component Structure**
*   Create `components/Dashboard/` folder.
*   Build the layout: `Sidebar`, `Header`, `MainContent`.

**Step 3: WebSocket Hook**
*   Create `hooks/useWebSocket.ts`.
*   Manage connection state (Connected/Disconnected/Reconnecting).
*   Expose `lastMessage` and `sendMessage` methods.

**Step 4: Build the Live Feed**
*   Use a mocked list of messages first to perfect the CSS.
*   Then connect it to `useWebSocket` to receive real data.

**Step 5: Add Visual Polish**
*   Implement "Dark Mode" by default.
*   Use Green/Red monospaced fonts for that "Cyber Security" look.

## 🧪 Testing
*   Run `npm run dev` and view locally.
*   Use a mock server or the actual backend to send test WebSocket events.
