import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# Hugging Face configuration
HF_API_KEY = os.getenv("HF_TOKEN")
HF_BASE_URL = "https://api-inference.huggingface.co/models"
DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"  # Free, fast model

def call_huggingface_api(prompt: str, technical_params: dict = None) -> dict:
    """
    Sends a request to the Hugging Face Inference API and handles the response.
    """
    if not HF_API_KEY:
        return {"error": "HF_TOKEN not found in environment variables. Please set your Hugging Face API token.", "status": "failed"}

    # Use technical parameters or defaults
    if technical_params is None:
        technical_params = {"width": 1024, "height": 1024, "guidance_scale": 7.5, "num_inference_steps": 4}

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Use FLUX.1-schnell model (free and fast)
    url = f"{HF_BASE_URL}/{DEFAULT_MODEL}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "guidance_scale": technical_params.get("guidance_scale", 7.5),
            "num_inference_steps": technical_params.get("num_inference_steps", 4),
            "width": technical_params.get("width", 1024),
            "height": technical_params.get("height", 1024)
        }
    }

    print(f"\nCalling Hugging Face API: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Model: {DEFAULT_MODEL}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Handle rate limiting with retries
        if response.status_code == 503:
            print("Model is loading, waiting...")
            time.sleep(10)  # Wait 10 seconds
            response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 429:
            print("Rate limit hit, waiting...")
            time.sleep(30)  # Wait 30 seconds for rate limit
            response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Successful response - return binary image data
            return {
                "status": "completed",
                "image_data": response.content,
                "content_type": response.headers.get("content-type", "image/png")
            }
        else:
            # Handle error responses
            try:
                error_details = response.json()
                print(f"API Error: {response.status_code} - {error_details}")
                return {
                    "error": f"HTTP {response.status_code}: {error_details.get('error', 'Unknown error')}",
                    "details": error_details,
                    "status": "failed"
                }
            except json.JSONDecodeError:
                print(f"Non-JSON error response: {response.text}")
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status": "failed"
                }
                
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return {"error": str(conn_err), "status": "failed"}
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return {"error": str(timeout_err), "status": "failed"}
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
        return {"error": str(req_err), "status": "failed"}

# Backward compatibility - keep the old function name
def call_runway_api(endpoint: str, payload: dict) -> dict:
    """
    Backward compatibility wrapper for call_huggingface_api.
    Converts RunwayML-style calls to Hugging Face format.
    """
    prompt = payload.get("promptText", payload.get("inputs", ""))
    
    # Extract technical parameters from payload
    technical_params = {
        "width": 1024,  # Default
        "height": 1024,  # Default
        "guidance_scale": 7.5,
        "num_inference_steps": 4
    }
    
    # Map RunwayML ratio to width/height
    if "ratio" in payload:
        ratio = payload["ratio"]
        if ratio == "16:9":
            technical_params.update({"width": 1024, "height": 576})
        elif ratio == "9:16":
            technical_params.update({"width": 576, "height": 1024})
        elif ratio == "4:3":
            technical_params.update({"width": 1024, "height": 768})
        # 1:1 remains 1024x1024
    
    return call_huggingface_api(prompt, technical_params)

def check_huggingface_setup() -> dict:
    """
    Check if Hugging Face API is properly configured.
    """
    if not HF_API_KEY:
        return {
            "status": "error",
            "message": "HF_TOKEN not found. Please set your Hugging Face API token.",
            "setup_instructions": [
                "1. Go to https://huggingface.co/settings/tokens",
                "2. Create a new token (read permission is sufficient)",
                "3. Set environment variable: HF_TOKEN=your_token_here",
                "4. Or create a .env file with: HF_TOKEN=your_token_here"
            ]
        }
    
    # Test API connection
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        test_url = f"{HF_BASE_URL}/{DEFAULT_MODEL}"
        response = requests.get(test_url, headers=headers)
        if response.status_code == 200:
            return {"status": "success", "message": "Hugging Face API is properly configured!"}
        else:
            return {"status": "warning", "message": f"API token works but model might be loading. Status: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Connection test failed: {e}"}

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Hugging Face API Communication ---")
    
    # Test setup first
    print("\nChecking Hugging Face setup...")
    setup_result = check_huggingface_setup()
    print(f"Setup Status: {setup_result}")
    
    if setup_result["status"] == "error":
        print("Please configure your Hugging Face API token before testing.")
        exit(1)

    # Test Case 1: Simple image generation
    print("\nTest Case 1: Simple Image Generation")
    simple_prompt = "A beautiful sunset over mountains, highly detailed, photorealistic"
    result1 = call_huggingface_api(simple_prompt)
    print(f"Result status: {result1.get('status')}")
    if result1.get('status') == 'completed':
        print(f"Image data size: {len(result1['image_data'])} bytes")
        print("✅ Image generation successful!")
    else:
        print(f"❌ Error: {result1.get('error')}")

    # Test Case 2: Custom parameters
    print("\nTest Case 2: Custom Parameters")
    custom_params = {
        "width": 1024,
        "height": 576,  # 16:9 aspect ratio
        "guidance_scale": 8.0,
        "num_inference_steps": 6
    }
    result2 = call_huggingface_api("A modern corporate office interior, professional lighting", custom_params)
    print(f"Result status: {result2.get('status')}")
    if result2.get('status') == 'completed':
        print("✅ Custom parameters test successful!")
    else:
        print(f"❌ Error: {result2.get('error')}")

    # Test Case 3: Backward compatibility
    print("\nTest Case 3: Backward Compatibility (RunwayML-style call)")
    runway_payload = {
        "promptText": "A vibrant infographic design, professional, modern",
        "ratio": "16:9",
        "model": "gen4_image"  # This will be ignored
    }
    result3 = call_runway_api("/v1/text_to_image", runway_payload)
    print(f"Result status: {result3.get('status')}")
    if result3.get('status') == 'completed':
        print("✅ Backward compatibility test successful!")
    else:
        print(f"❌ Error: {result3.get('error')}")

    print("\nAPI communication tests completed!")