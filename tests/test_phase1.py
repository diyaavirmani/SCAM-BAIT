
import sys
import os
import asyncio
import httpx
import websockets
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.extraction import extract_intelligence

async def test_extraction():
    print("\n[TEST 1] Testing Enhanced Extraction Logic...")
    
    scam_text = """
    URGENT! Your verified account is blocked. 
    Download our security app at http://secure-bank-app.com/update.apk immediately.
    Send your details to support@axis-verify.com.
    Or contact us on Telegram @SBI_Support_Official.
    Please transfer ₹10,000 to Bitcoin wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.
    IFSC: SBIN0001234
    """
    
    intel = extract_intelligence([{"text": scam_text}])
    
    print(f"-> Extracted Emails: {intel.get('emails')}")
    print(f"-> Extracted APKs: {intel.get('apkLinks')}")
    print(f"-> Extracted Crypto: {intel.get('cryptoWallets')}")
    print(f"-> Extracted Social: {intel.get('socialHandles')}")
    print(f"-> Extracted IFSC: {intel.get('ifscCodes')}")
    
    assert len(intel['emails']) > 0, "Failed to extract Email"
    assert len(intel['apkLinks']) > 0, "Failed to extract APK Link"
    assert len(intel['cryptoWallets']) > 0, "Failed to extract Crypto Wallet"
    assert len(intel['socialHandles']) > 0, "Failed to extract Social Handle"
    assert len(intel['ifscCodes']) > 0, "Failed to extract IFSC Code"
    print("✅ Extraction Test Passed!")

async def test_api_endpoints():
    print("\n[TEST 2] Testing API Endpoints...")
    async with httpx.AsyncClient(base_url="http://localhost:8002") as client:
        # Test Stats
        try:
            resp = await client.get("/api/v1/stats")
            print(f"-> GET /stats Response: {resp.status_code}")
            print(f"-> Stats Data: {resp.json()}")
            assert resp.status_code == 200
            print("✅ Stats API Test Passed!")
        except Exception as e:
             print(f"❌ API Test Failed (Is server running?): {e}")

async def test_websocket():
    print("\n[TEST 3] Testing WebSocket Connection...")
    uri = "ws://localhost:8002/ws/dashboard"
    try:
        async with websockets.connect(uri) as websocket:
            print("-> Connected to WebSocket")
            await websocket.send("ping")
            response = await websocket.recv()
            print(f"-> Received: {response}")
            assert response == "pong"
            print("✅ WebSocket Test Passed!")
    except Exception as e:
        print(f"❌ WebSocket Test Failed (Is server running?): {e}")

async def main():
    print("="*50)
    print("PHASE 1 VERIFICATION STARTED")
    print("="*50)
    
    # Unit Test Extraction (No server needed)
    await test_extraction()
    
    # Integration Tests (Server needed)
    print("\n⚠️ Note: Ensure 'python run.py' is running in another terminal for API/WS tests.\n")
    await test_api_endpoints()
    await test_websocket()

if __name__ == "__main__":
    asyncio.run(main())
