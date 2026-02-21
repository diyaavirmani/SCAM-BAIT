import requests
import sys

# Default to production URL
DEFAULT_URL = "https://honey-api-wr74.onrender.com/voice/incoming"

def test_webhook(url=DEFAULT_URL):
    print(f"Testing Webhook at: {url}")
    
    # Simulate Twilio POST data
    payload = {
        "CallSid": "CA1234567890abcdef1234567890abcdef",
        "From": "+15551234567",
        "To": "+15557654321",
        "Direction": "inbound",
        "ApiVersion": "2010-04-01",
        "AccountSid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

    try:
        response = requests.post(url, data=payload)
        
        print(f"\nStatus Code: {response.status_code}")
        print("\nResponse Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
            
        print("\nResponse Body (TwiML):")
        print(response.text)
        
        if "<Response>" in response.text and "<Connect>" in response.text:
            print("\n✅ SUCCESS: Valid TwiML response received!")
            print("The webhook is correctly configured to accept calls and redirect to the media stream.")
        else:
            print("\n❌ WARNING: Response doesn't look like valid TwiML.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    test_webhook(target_url)
