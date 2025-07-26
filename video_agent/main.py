import time
from video_agent.video_creation import start_video_generation, check_generation_status
from video_agent.customization import set_seed, set_duration
from video_agent.enhancements import set_ratio, enable_watermark

def run_video_workflow(prompt, title, custom_options=None):
    """
    A generic workflow to start a video generation task and poll for its result.
    """
    print(f"\n--- Running Workflow: {title} ---")
    print(f"  - Prompt: '{prompt}'")
    
    if custom_options:
        print("  - With custom options:")
        for key, value in custom_options.items():
            print(f"    - {key}: {value}")

    try:
        # 1. Start the generation task
        start_response = start_video_generation(prompt, options=custom_options)
        task_uuid = start_response.get("uuid")
        
        if not task_uuid:
            raise Exception(f"Failed to get task UUID from response: {start_response}")
            
        print(f"\n  -> Task started successfully with UUID: {task_uuid}")

        # 2. Poll for the result
        while True:
            print("  -> Checking task status...")
            status_response = check_generation_status(task_uuid)
            status = status_response.get("status")
            
            print(f"  -> Current status: {status}")
            
            if status == "SUCCEEDED":
                video_url = status_response.get("output", {}).get("url")
                print(f"\n  -> Generation Succeeded! Video URL: {video_url}")
                # In a real app, you'd save this URL to a database or pass it on.
                return video_url
            elif status == "FAILED":
                error_msg = status_response.get('error_message', 'No error message provided.')
                print(f"\n  -> Generation Failed! Reason: {error_msg}")
                return None
            
            # Wait before checking again
            time.sleep(15)

    except Exception as e:
        print(f"\nAn error occurred during the workflow: {e}")
        return None

if __name__ == "__main__":
    # --- Workflow 1: Sci-Fi Scene ---
    # A simple prompt with default settings.
    run_video_workflow(
        prompt="A futuristic cityscape at night, with flying vehicles and neon signs.",
        title="Sci-Fi Cityscape"
    )

    # --- Workflow 2: Nature Scene with Customization ---
    # A more specific prompt with custom seed and duration.
    nature_options = {}
    nature_options.update(set_seed(123))
    nature_options.update(set_duration(10))
    nature_options.update(enable_watermark(False))
    run_video_workflow(
        prompt="A tranquil forest stream flowing over mossy rocks, sunlight filtering through the trees.",
        title="Quiet Forest Stream",
        custom_options=nature_options
    )

    # --- Workflow 3: High-Resolution Abstract Animation ---
    # A prompt for something abstract, with a specific ratio.
    abstract_options = {}
    abstract_options.update(set_ratio("1:1"))
    run_video_workflow(
        prompt="Colorful liquid ink spreading and mixing in water, creating abstract patterns, macro shot.",
        title="Abstract Ink Animation",
        custom_options=abstract_options
    )