import json
import sys
import os
from datetime import datetime

# Add the project root to the sys.path to allow importing graphics_agent.main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphics_agent.main import generate_graphic
from pydantic import BaseModel # For defining the request model structure

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "endpoint_test_log.txt")

# Re-define the request model here for self-contained testing
class GraphicsGenerationRequest(BaseModel):
    text_description: str
    content_type: str = None
    data: dict = None
    style_params: dict = None
    technical_params: dict = None
    data_params: dict = None

def log_test_result(test_name: str, input_data: dict, output_data: any, error: str = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n--- Test Case: {test_name} ({timestamp}) ---\n")
        f.write(f"Input:\n{json.dumps(input_data, indent=2)}\n")
        if error:
            f.write(f"Error:\n{error}\n")
        else:
            f.write(f"Output:\n{json.dumps(output_data, indent=2)}\n")
        f.write("----------------------------------------\n")

async def run_endpoint_tests():
    print(f"Running endpoint tests. Logs will be written to: {LOG_FILE}")

    # Clear log file for a fresh run
    with open(LOG_FILE, "w") as f:
        f.write(f"Endpoint Test Log - Started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")

    # Test Case 1: Successful Infographic Generation
    test_name = "Successful Infographic Generation"
    input_data = {
        "text_description": "Create a quarterly sales performance infographic showing 25% growth with modern corporate styling",
        "content_type": "infographics",
        "style_params": {"style": "corporate", "color_scheme": "brand_primary"},
        "data": {"Q1": 100, "Q2": 125, "Q3": 156.25}
    }
    request_obj = GraphicsGenerationRequest(**input_data)
    try:
        # Directly call the core logic function
        response = generate_graphic(
            text_description=request_obj.text_description,
            content_type=request_obj.content_type,
            data=request_obj.data,
            style_params=request_obj.style_params,
            technical_params=request_obj.technical_params,
            data_params=request_obj.data_params
        )
        log_test_result(test_name, input_data, response)
    except Exception as e:
        log_test_result(test_name, input_data, None, f"Error: {e}")

    # Test Case 2: Successful Storyboard Generation
    test_name = "Successful Storyboard Generation"
    input_data = {
        "text_description": "Generate a 4-panel storyboard showing customer onboarding process in friendly, approachable style",
        "content_type": "storyboards",
        "style_params": {"tone": "friendly", "complexity": "simple"},
        "technical_params": {"dimensions": "1280:720"}
    }
    request_obj = GraphicsGenerationRequest(**input_data)
    try:
        response = generate_graphic(
            text_description=request_obj.text_description,
            content_type=request_obj.content_type,
            data=request_obj.data,
            style_params=request_obj.style_params,
            technical_params=request_obj.technical_params,
            data_params=request_obj.data_params
        )
        log_test_result(test_name, input_data, response)
    except Exception as e:
        log_test_result(test_name, input_data, None, f"Error: {e}")

    # Test Case 3: Invalid Content Type
    test_name = "Invalid Content Type"
    input_data = {
        "text_description": "Some text",
        "content_type": "unsupported_type"
    }
    request_obj = GraphicsGenerationRequest(**input_data)
    try:
        response = generate_graphic(
            text_description=request_obj.text_description,
            content_type=request_obj.content_type,
            data=request_obj.data,
            style_params=request_obj.style_params,
            technical_params=request_obj.technical_params,
            data_params=request_obj.data_params
        )
        log_test_result(test_name, input_data, response)
    except Exception as e:
        log_test_result(test_name, input_data, None, f"Error: {e}")

    # Test Case 4: Simulated API Error (due to prompt content)
    test_name = "Simulated API Error"
    input_data = {
        "text_description": "Create an image with an error in the prompt to trigger API failure.",
        "content_type": "illustrations"
    }
    request_obj = GraphicsGenerationRequest(**input_data)
    try:
        response = generate_graphic(
            text_description=request_obj.text_description,
            content_type=request_obj.content_type,
            data=request_obj.data,
            style_params=request_obj.style_params,
            technical_params=request_obj.technical_params,
            data_params=request_obj.data_params
        )
        log_test_result(test_name, input_data, response)
    except Exception as e:
        log_test_result(test_name, input_data, None, f"Error: {e}")

    print("Endpoint tests completed. Check the log file for details.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_endpoint_tests())