import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
RUNWAY_BASE_URL = "https://api.dev.runwayml.com"

def call_runway_api(endpoint: str, payload: dict) -> dict:
    """
    Sends a request to the RunwayML API and handles the response.
    """
    if not RUNWAY_API_KEY:
        return {"error": "RUNWAY_API_KEY not found in environment variables.", "status": "failed"}

    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
        "X-Runway-Version": "2024-11-06"
    }
    url = f"{RUNWAY_BASE_URL}{endpoint}"

    print(f"\nCalling RunwayML API: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        try:
            error_details = http_err.response.json()
            print(f"Response content: {error_details}")
            return {"error": str(http_err), "details": error_details, "status": "failed"}
        except json.JSONDecodeError:
            print(f"Response content (non-JSON): {http_err.response.text}")
            return {"error": str(http_err), "details": http_err.response.text, "status": "failed"}
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return {"error": str(conn_err), "status": "failed"}
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return {"error": str(timeout_err), "status": "failed"}
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
        return {"error": str(req_err), "status": "failed"}

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing API Communication (Real) ---")

    # Test Case 1: Simulate successful image generation (requires a valid prompt for RunwayML)
    print("\nTest Case 1: Attempting Image Generation")
    image_payload = {"prompt": "A serene landscape with a distant mountain range, highly detailed, photorealistic", "model": "stable-diffusion-v1-5"}
    image_result = call_runway_api("/image/generate", image_payload)
    print(f"Result: {json.dumps(image_result, indent=2)}")
    # Expecting 'status' to be 'pending' or 'completed' in a real scenario
    # For testing, we'll just check for the presence of 'id' or 'error'
    assert "id" in image_result or "error" in image_result

    # Test Case 2: Simulate successful video generation (requires a valid prompt for RunwayML)
    print("\nTest Case 2: Attempting Video Generation")
    video_payload = {"prompt": "A short animation of a futuristic car driving on a highway, cinematic, 4k", "model": "gen-1"}
    video_result = call_runway_api("/video/generate", video_payload)
    print(f"Result: {json.dumps(video_result, indent=2)}")
    assert "id" in video_result or "error" in video_result

    # Test Case 3: Simulate API error (e.g., invalid model or prompt)
    print("\nTest Case 3: Attempting API Error (Invalid Model)")
    error_payload = {"prompt": "A simple drawing", "model": "non-existent-model"}
    error_result = call_runway_api("/image/generate", error_payload)
    print(f"Result: {json.dumps(error_result, indent=2)}")
    assert error_result.get("status") == "failed"
    assert "error" in error_result

    print("\nAPI communication tests (real) completed. Check logs for actual API responses.")