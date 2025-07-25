import requests
import json
import datetime

# Base URL for the running FastAPI application
BASE_URL = "http://127.0.0.1:8000"
LOG_FILE = "voice_logs.txt"

def log_interaction(endpoint, request_data, response, error=None):
    """Logs the details of an API interaction to the log file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"--- Interaction Log: {datetime.datetime.now()} ---\n")
        f.write(f"Endpoint: {endpoint}\n")
        f.write(f"Request Data:\n{json.dumps(request_data, indent=2)}\n")
        if response is not None:
            f.write(f"Response Status Code: {response.status_code}\n")
            f.write(f"Response Body:\n{json.dumps(response.json(), indent=2)}\n")
        if error:
            f.write(f"Error: {error}\n")
        f.write("-" * 50 + "\n\n")

def test_list_voices():
    """Tests the /list-voices endpoint."""
    endpoint = "/list-voices"
    print(f"Testing {endpoint}...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        log_interaction(endpoint, {}, response)
        print("Success.")
    except requests.exceptions.RequestException as e:
        log_interaction(endpoint, {}, None, error=str(e))
        print(f"Failed: {e}")

def test_generate_audio():
    """Tests the /generate-audio endpoint."""
    endpoint = "/generate-audio"
    print(f"Testing {endpoint}...")
    request_data = {
        "text": "Hello, this is a test from the test script.",
        "output_path": "test_script_basic.mp3"
    }
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=request_data)
        response.raise_for_status()
        log_interaction(endpoint, request_data, response)
        print("Success.")
    except requests.exceptions.RequestException as e:
        log_interaction(endpoint, request_data, None, error=str(e))
        print(f"Failed: {e}")

def test_generate_modulated_audio():
    """Tests the /generate-modulated-audio endpoint."""
    endpoint = "/generate-modulated-audio"
    print(f"Testing {endpoint}...")
    request_data = {
        "text": "This is a test of modulated audio.",
        "output_path": "test_script_modulated.mp3",
        "stability": 0.6,
        "similarity_boost": 0.6
    }
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=request_data)
        response.raise_for_status()
        log_interaction(endpoint, request_data, response)
        print("Success.")
    except requests.exceptions.RequestException as e:
        log_interaction(endpoint, request_data, None, error=str(e))
        print(f"Failed: {e}")

def test_generate_in_language():
    """Tests the /generate-in-language endpoint."""
    endpoint = "/generate-in-language"
    print(f"Testing {endpoint}...")
    request_data = {
        "text": "Bonjour, ceci est un test en français.",
        "language_labels": {"accent": "french"},
        "output_path": "test_script_french.mp3"
    }
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=request_data)
        response.raise_for_status()
        log_interaction(endpoint, request_data, response)
        print("Success.")
    except requests.exceptions.RequestException as e:
        log_interaction(endpoint, request_data, None, error=str(e))
        print(f"Failed: {e}")

def test_generate_with_ambience():
    """Tests the /generate-with-ambience endpoint."""
    endpoint = "/generate-with-ambience"
    print(f"Testing {endpoint}...")
    # Ensure a dummy ambience file exists
    try:
        from pydub import AudioSegment
        import os
        if not os.path.exists("news_studio.mp3"):
            AudioSegment.silent(duration=5000).export("news_studio.mp3", format="mp3")
    except Exception as e:
        print(f"Could not create dummy ambience file: {e}")

    request_data = {
        "text": "Testing ambience from the test script.",
        "ambience_file": "news_studio.mp3",
        "output_path": "test_script_ambience.mp3"
    }
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=request_data)
        response.raise_for_status()
        log_interaction(endpoint, request_data, response)
        print("Success.")
    except requests.exceptions.RequestException as e:
        log_interaction(endpoint, request_data, None, error=str(e))
        print(f"Failed: {e}")

if __name__ == "__main__":
    print("--- Starting API Endpoint Tests ---")
    # Clear the log file for a fresh start
    with open(LOG_FILE, "w") as f:
        f.write("API Test Logs\n" + "="*50 + "\n\n")
    
    test_list_voices()
    test_generate_audio()
    test_generate_modulated_audio()
    test_generate_in_language()
    test_generate_with_ambience()
    
    print("\n--- API Endpoint Tests Complete ---")
    print(f"All interactions have been logged to {LOG_FILE}")