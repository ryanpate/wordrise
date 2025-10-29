"""
WordRise API Test Script

Tests all API endpoints to ensure they work correctly
"""
import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(f"Status: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def test_api():
    """Test all API endpoints"""
    
    print("\n🏗️  WORDRISE API TEST")
    print("="*60)
    
    # Test 1: Health check
    print("\n1️⃣  Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    # Test 2: Get daily word
    print("\n2️⃣  Testing daily word...")
    response = requests.get(f"{BASE_URL}/daily/word")
    print_response("Daily Word", response)
    daily_word = response.json()['word']
    
    # Test 3: Start a new game (practice mode)
    print("\n3️⃣  Testing game start (practice mode)...")
    response = requests.post(
        f"{BASE_URL}/game/start",
        json={"mode": "practice", "starting_word": "art"}
    )
    print_response("Start Game", response)
    session_id = response.json()['session_id']
    
    # Test 4: Get game state
    print("\n4️⃣  Testing get game state...")
    response = requests.get(f"{BASE_URL}/game/{session_id}/state")
    print_response("Game State", response)
    
    # Test 5: Add a word
    print("\n5️⃣  Testing add word...")
    response = requests.post(
        f"{BASE_URL}/game/{session_id}/add-word",
        json={"word": "tart"}
    )
    print_response("Add Word 'tart'", response)
    
    # Test 6: Add another word
    print("\n6️⃣  Testing add another word...")
    response = requests.post(
        f"{BASE_URL}/game/{session_id}/add-word",
        json={"word": "start"}
    )
    print_response("Add Word 'start'", response)
    
    # Test 7: Get hint
    print("\n7️⃣  Testing hint system...")
    response = requests.get(f"{BASE_URL}/game/{session_id}/hint?hint_type=starts_with")
    print_response("Get Hint", response)
    
    # Test 8: Try invalid word
    print("\n8️⃣  Testing invalid word...")
    response = requests.post(
        f"{BASE_URL}/game/{session_id}/add-word",
        json={"word": "xyz"}
    )
    print_response("Invalid Word 'xyz'", response)
    
    # Test 9: Undo word
    print("\n9️⃣  Testing undo...")
    response = requests.post(f"{BASE_URL}/game/{session_id}/undo")
    print_response("Undo Last Word", response)
    
    # Test 10: End game
    print("\n🔟  Testing end game...")
    response = requests.post(f"{BASE_URL}/game/{session_id}/end")
    print_response("End Game", response)
    
    # Test 11: Validate word
    print("\n1️⃣1️⃣  Testing word validation...")
    response = requests.post(
        f"{BASE_URL}/validate-word",
        json={"word": "hello"}
    )
    print_response("Validate Word", response)
    
    # Test 12: Get server stats
    print("\n1️⃣2️⃣  Testing server stats...")
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Server Stats", response)
    
    # Test 13: Start daily challenge
    print("\n1️⃣3️⃣  Testing daily challenge...")
    response = requests.post(
        f"{BASE_URL}/game/start",
        json={"mode": "daily"}
    )
    print_response("Start Daily Challenge", response)
    daily_session_id = response.json()['session_id']
    
    print("\n" + "="*60)
    print("✅ All API tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the Flask server is running:")
        print("  python3 run.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
