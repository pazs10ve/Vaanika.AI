import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_BASE_URL = "https://api.runwayml.com/v1"
API_KEY = os.getenv("RUNWAY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def start_video_generation(prompt, options=None):
    """
    Starts the video generation process by making a POST request to the Runway ML API.
    """
    if options is None:
        options = {}
    
    # All parameters are at the top level of the JSON body.
    payload = {
        "model": "gen-2",
        "promptText": prompt,
        **options
    }

    url = f"{API_BASE_URL}/tasks"
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"RunwayML API Error: {e.response.status_code} - {e.response.text}")
        raise e

def check_generation_status(task_uuid):
    """
    Checks the status of a video generation task by its UUID.

    Args:
        task_uuid (str): The UUID of the task to check.

    Returns:
        dict: The JSON response from the API with the task's status.
    """
    url = f"{API_BASE_URL}/tasks/{task_uuid}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    test_prompt = "A cinematic shot of a lone astronaut walking on a desolate, red-hued alien planet."
    
    print("--- Testing Runway ML API Video Generation ---")
    try:
        # 1. Start the generation task
        print("Starting video generation...")
        start_response = start_video_generation(test_prompt, options={"duration": 5})
        
        task_uuid = start_response.get("uuid")
        if not task_uuid:
            raise Exception(f"Failed to get task UUID. Response: {start_response}")
            
        print(f"Task started with UUID: {task_uuid}")

        # 2. Poll for the result
        while True:
            import time
            print("Checking task status...")
            status_response = check_generation_status(task_uuid)
            status = status_response.get("status")
            
            print(f"Current status: {status}")
            
            if status == "SUCCEEDED":
                video_url = status_response.get("output", {}).get("url")
                print(f"Generation Succeeded! Video URL: {video_url}")
                break
            elif status == "FAILED":
                error_msg = status_response.get('error_message', 'No error message provided.')
                print(f"Generation Failed! Reason: {error_msg}")
                break
            
            time.sleep(10)

    except requests.exceptions.RequestException as e:
        print(f"An API error occurred: {e}")
        if e.response:
            print(f"Response body: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")