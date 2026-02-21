import asyncio
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.detection import detect_scam, detect_scam_type

async def test_scam_type_classification():
    print("\n[TEST] Verifying Scam Type Classification...")
    
    test_cases = [
        ("Your fedex parcel contains illegal drugs. Police will arrest you.", "DIGITAL_ARREST"),
        ("You received a cashback of Rs 500. Scan QR to receive.", "UPI_SCAM"),
        ("Part time job work from home. Earn 5000 daily.", "JOB_SCAM"),
        ("I have your video recording. Pay me or I leak it.", "SEXTORTION"),
        ("Congratulations you won a lottery prize of 1 crore.", "LOTTERY_SCAM"),
        ("Hello, how are you?", "NONE") # Should be safe
    ]
    
    for text, expected_type in test_cases:
        is_scam, confidence, scam_type = await detect_scam(text)
        print(f"Text: '{text[:40]}...'")
        print(f" -> Result: Scam={is_scam}, Type={scam_type}")
        
        if expected_type == "NONE":
            assert not is_scam, f"Expected SAFE, got SCAM for '{text}'"
        else:
            assert is_scam, f"Expected SCAM, got SAFE for '{text}'"
            assert scam_type == expected_type, f"Expected {expected_type}, got {scam_type}"
            
    print("✅ Scam Type Verification Passed!")

if __name__ == "__main__":
    asyncio.run(test_scam_type_classification())
