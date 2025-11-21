"""
Test script to verify Gemini API key is working
Run this to test if your API key is configured correctly
"""
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

if not API_KEY:
    print("❌ GEMINI_API_KEY not found!")
    print("   Please create a .env file in the backend/ directory with:")
    print("   GEMINI_API_KEY=your_api_key_here")
    exit(1)

print(f"✅ API Key found: {API_KEY[:10]}...{API_KEY[-5:]}")
print("🧪 Testing Gemini API...")

try:
    params = {"key": API_KEY}
    data = {
        "contents": [{
            "parts": [{
                "text": "Hello! Can you tell me about plant care?"
            }]
        }]
    }
    
    resp = requests.post(GEMINI_URL, params=params, json=data, timeout=30)
    
    if resp.status_code == 200:
        response_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        print("✅ SUCCESS! Gemini API is working!")
        print(f"\nResponse: {response_text[:200]}...")
    else:
        print(f"❌ API Error - Status Code: {resp.status_code}")
        print(f"Response: {resp.text}")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")

