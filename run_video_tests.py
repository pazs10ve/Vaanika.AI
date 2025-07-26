import requests
import time
import json
import os

# --- Test Configuration ---
BASE_URL = "http://127.0.0.1:8000"
LOG_FILE = "video_agent/logs/video_test_log.txt"
OUTPUT_DIR = "video_agent/outputs"

TEST_CASES = [
    {
        "title": "Simple Video Generation",
        "payload": {"prompt_text": "a cat driving a car"}
    },
    {
        "title": "Video with Seed",
        "payload": {"prompt_text": "a dog riding a skateboard", "seed": 12345}
    },
    {
        "title": "Video with Duration and Watermark",
        "payload": {"prompt_text": "a bird flying in the sky", "duration": 10, "watermark": True}
    },
    {
        "title": "Video with Custom Ratio",
        "payload": {"prompt_text": "a robot dancing", "ratio": "1:1"}
    }
]

def log_message(message, overwrite=False):
    mode = "w" if overwrite else "a"
    with open(LOG_FILE, mode) as f:
        f.write(message + "\n")

def run_test(title, payload):
    log_message(f"--- Test Case: {title} ---")
    log_message(f"Request Payload: {json.dumps(payload)}")

    try:
        # Start generation
        response = requests.post(f"{BASE_URL}/video/generate", json=payload)
        response.raise_for_status()
        task_info = response.json()
        task_id = task_info.get("task_id")
        log_message(f"Generation Started: {task_info}")

        if not task_id:
            log_message("Error: Task ID not found in response.")
            return

        # Poll for status
        while True:
            time.sleep(10)
            status_response = requests.get(f"{BASE_URL}/video/status/{task_id}")
            status_info = status_response.json()
            status = status_info.get("status")
            log_message(f"Polling Status: {status}")

            if status == "SUCCEEDED":
                log_message(f"Generation Succeeded: {status_info}")
                output_url = status_info.get("output", {}).get("url")
                if output_url:
                    # Save the output
                    output_filename = os.path.join(OUTPUT_DIR, f"{title.replace(' ', '_').lower()}.json")
                    with open(output_filename, "w") as f:
                        json.dump(status_info, f, indent=4)
                    log_message(f"Output saved to {output_filename}")
                break
            elif status == "FAILED":
                log_message(f"Generation Failed: {status_info}")
                break

    except requests.exceptions.RequestException as e:
        log_message(f"Error during test: {e}")

if __name__ == "__main__":
    # Overwrite the log file at the start of the test run
    log_message("--- Starting Video Generation Test Run ---", overwrite=True)
    for test in TEST_CASES:
        run_test(test["title"], test["payload"])