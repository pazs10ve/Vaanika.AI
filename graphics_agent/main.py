from .input_processing import process_input
from .prompt_generation import generate_runway_prompt
from .api_communication import call_runway_api
from .output_delivery import deliver_output
import json

def generate_graphic(text_description: str, content_type: str = None, data: dict = None, style_params: dict = None, technical_params: dict = None, data_params: dict = None):
    """
    End-to-end workflow for generating graphics using RunwayML.
    """
    print(f"\n--- Generating Graphic for: {text_description} ---")
    try:
        # 1. Input Processing
        processed_input = process_input(text_description, content_type, data, style_params, technical_params, data_params)
        print("Input Processed.")

        # Map aspect ratio to concrete dimensions for RunwayML's 'ratio' parameter
        aspect_ratio_map = {
            "16:9": "1920:1080",
            "4:3": "1024:768",
            "1:1": "1024:1024",
            "9:16": "1080:1920",
            "square": "1024:1024",
            "portrait": "1080:1920",
            "landscape": "1920:1080"
        }
        # Determine the ratio for RunwayML API based on the aspect_ratio parameter
        # Default to "1024:1024" if aspect_ratio is not provided or not in map
        runway_ratio = aspect_ratio_map.get(processed_input["technical_parameters"].get("aspect_ratio"), "1024:1024")

        # 2. Prompt Generation
        runway_prompt = generate_runway_prompt(processed_input)
        print(f"RunwayML Prompt Generated: {runway_prompt}")

        # Determine API endpoint based on content type
        api_endpoint = "/v1/text_to_image"
        api_payload = {
            "promptText": runway_prompt,
            "ratio": runway_ratio
        }

        if processed_input["content_type"] == "storyboards":
            api_endpoint = "/v1/image_to_video"
            api_payload["model"] = "gen4_turbo" # Recommended model for image_to_video
            # For image_to_video, a promptImage is required.
            # Using a publicly accessible placeholder image for testing purposes.
            # In a real scenario, this would be the output_url from a prior image generation step.
            api_payload["promptImage"] = "https://www.nasa.gov/sites/default/files/thumbnails/image/iss068e050000.jpg" # Example public image
            api_payload["duration"] = 4 # seconds
            # Remove promptText if image_to_video doesn't primarily use it, or adjust as per API
            # RunwayML docs suggest both promptImage and promptText for image_to_video
        else:
            api_payload["model"] = "gen4_image" # Recommended model for text_to_image

        # 3. API Communication
        api_response = call_runway_api(api_endpoint, api_payload)
        print("API Communication Complete.")

        # 4. Output Delivery
        output_url = deliver_output(api_response)
        print(f"Generated Graphic URL: {output_url}")
        return output_url

    except Exception as e:
        print(f"An error occurred during graphic generation: {e}")
        return None

# --- Example Workflows (from prompt.txt) ---
if __name__ == "__main__":
    print("--- Running Example Workflows ---")

    # Example 1: Business Infographic
    generate_graphic(
        text_description="Create a quarterly sales performance infographic showing 25% growth.",
        content_type="infographics",
        style_params={"style": "corporate", "color_scheme": "brand_primary"},
        data_params={"data_source": "inline_json"}, # Assuming data is implicitly in description for this example
        data={
            "title": "Quarterly Sales Performance",
            "metrics": [
                {"quarter": "Q1", "sales": 100, "growth": "5%"},
                {"quarter": "Q2", "sales": 105, "growth": "5%"},
                {"quarter": "Q3", "sales": 131.25, "growth": "25%"},
                {"quarter": "Q4", "sales": 137.81, "growth": "5%"}
            ]
        },
        technical_params={"aspect_ratio": "16:9"}
    )

    # Example 2: Process Storyboard
    generate_graphic(
        text_description="Generate a 4-panel storyboard showing customer onboarding process.",
        content_type="storyboards",
        style_params={"tone": "friendly", "complexity": "simple"},
        technical_params={"aspect_ratio": "16:9"}
    )

    # Example 3: Data Visualization (Pie Chart)
    generate_graphic(
        text_description="Convert this data into a vibrant pie chart showing market share distribution.",
        content_type="charts",
        style_params={"color_scheme": "vibrant"},
        data_params={"chart_type": "pie", "data_source": "inline_json"},
        data={
            "labels": ["Product A", "Product B", "Product C", "Product D"],
            "values": [40, 30, 20, 10]
        },
        technical_params={"aspect_ratio": "1:1"}
    )

    print("\n--- All Example Workflows Completed ---")