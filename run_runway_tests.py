import requests
import json
import os
import time
from datetime import datetime

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
GENERATE_ENDPOINT = "/video/generate"
STATUS_ENDPOINT = "/video/status"
LOG_DIR = "video_agent_tests/logs"
LOG_FILE = os.path.join(LOG_DIR, f"runway_test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
POLL_INTERVAL = 15  # seconds

# --- Test Cases ---
test_cases = [
    {
        "title": "Test 1: Simple Generation",
        "payload": {
            "script": "A photorealistic video of a cat playing with a ball of yarn in a sunlit living room."
        }
    },
    {
        "title": "Test 2: Generation with Seed",
        "payload": {
            "script": "An oil painting of a stormy sea coming to life.",
            "seed": 42
        }
    },
    {
        "title": "Test 3: Generation with Custom Motion",
        "payload": {
            "script": "A slow-motion shot of a hummingbird hovering next to a flower.",
            "motion": 3
        }
    }
]

# --- Test Execution ---
def run_tests():
    """Runs all defined test cases and logs the results."""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"--- Runway ML Video Generation Test Log ---\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write("="*50 + "\n\n")

        for i, test in enumerate(test_cases):
            print(f"--- Running {test['title']} ---")
            f.write(f"--- Test Case {i+1}: {test['title']} ---\n")
            
            task_id = None
            try:
                # 1. Start the generation task
                f.write("Request Payload:\n")
                f.write(json.dumps(test['payload'], indent=2) + "\n\n")
                
                start_response = requests.post(
                    f"{BASE_URL}{GENERATE_ENDPOINT}",
                    data=json.dumps(test['payload']),
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                f.write(f"Start Response Status: {start_response.status_code}\n")
                start_data = start_response.json()
                f.write("Start Response Body:\n")
                f.write(json.dumps(start_data, indent=2) + "\n\n")

                if start_response.status_code != 200:
                    raise Exception("Failed to start task.")

                task_id = start_data.get("task_id")
                if not task_id:
                    raise Exception("No task_id received from the API.")
                
                print(f"  -> Task started with ID: {task_id}")

                # 2. Poll for the result
                f.write(f"Polling status for task_id: {task_id}\n")
                while True:
                    print(f"  -> Checking status...")
                    status_response = requests.get(f"{BASE_URL}{STATUS_ENDPOINT}/{task_id}", timeout=30)
                    status_data = status_response.json()
                    status = status_data.get("status")
                    
                    f.write(f"  - Status at {datetime.now().isoformat()}: {status}\n")
                    print(f"  -> Status is: {status}")

                    if status == "SUCCEEDED":
                        f.write("\nGeneration Succeeded!\n")
                        f.write("Final Response Body:\n")
                        f.write(json.dumps(status_data, indent=2) + "\n")
                        print("  -> Success!")
                        break
                    elif status == "FAILED":
                        f.write("\nGeneration Failed!\n")
                        f.write("Final Response Body:\n")
                        f.write(json.dumps(status_data, indent=2) + "\n")
                        print("  -> Failure!")
                        break
                    
                    time.sleep(POLL_INTERVAL)

            except Exception as e:
                error_message = f"An error occurred: {e}"
                print(f"  -> ERROR: {error_message}")
                f.write(f"\nERROR: {error_message}\n")
            
            f.write("\n" + "="*50 + "\n\n")
            print(f"--- Finished {test['title']} ---\n")

if __name__ == "__main__":
    run_tests()
    print(f"All tests completed. Log file created at: {LOG_FILE}")
