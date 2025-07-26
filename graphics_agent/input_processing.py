import json

def process_input(text_description: str, content_type: str = None, data: dict = None, style_params: dict = None, technical_params: dict = None, data_params: dict = None):
    """
    Processes user input for graphics generation, applying defaults where necessary.
    """
    
    # Default style parameters
    default_style = {
        "style": "modern",
        "color_scheme": "brand_primary",
        "tone": "professional",
        "complexity": "simple"
    }
    
    # Default technical parameters
    default_technical = {
        "dimensions": "1024x1024",
        "format": "PNG",
        "resolution": "standard",
        "aspect_ratio": "1:1"
    }

    # Default data parameters (for charts/infographics)
    default_data = {
        "data_source": "inline_json",
        "chart_type": "bar",
        "data_labels": True,
        "legend_position": "bottom"
    }

    # Merge provided parameters with defaults
    processed_style = {**default_style, **(style_params if style_params else {})}
    processed_technical = {**default_technical, **(technical_params if technical_params else {})}
    processed_data = {**default_data, **(data_params if data_params else {})}

    # Validate content type
    supported_content_types = ["infographics", "charts", "illustrations", "storyboards"]
    if content_type and content_type not in supported_content_types:
        raise ValueError(f"Unsupported content type: {content_type}. Supported types are: {', '.join(supported_content_types)}")

    # Basic validation for data integration (more complex validation would be needed for real CSV/API)
    if data and not isinstance(data, dict):
        try:
            data = json.loads(data) # Try to parse if it's a JSON string
        except json.JSONDecodeError:
            raise ValueError("Data must be a dictionary or a valid JSON string.")

    return {
        "text_description": text_description,
        "content_type": content_type,
        "data": data,
        "style_parameters": processed_style,
        "technical_parameters": processed_technical,
        "data_parameters": processed_data
    }

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Input Processing ---")

    # Test Case 1: Basic input with defaults
    print("\nTest Case 1: Basic input with defaults")
    input1 = process_input("A simple illustration of a cat.")
    print(json.dumps(input1, indent=2))
    assert input1["text_description"] == "A simple illustration of a cat."
    assert input1["content_type"] is None
    assert input1["style_parameters"]["style"] == "modern"

    # Test Case 2: Specific content type and some custom style
    print("\nTest Case 2: Specific content type and some custom style")
    input2 = process_input(
        "Create a corporate infographic about Q3 sales.",
        content_type="infographics",
        style_params={"style": "corporate", "color_scheme": "high_contrast"}
    )
    print(json.dumps(input2, indent=2))
    assert input2["content_type"] == "infographics"
    assert input2["style_parameters"]["style"] == "corporate"
    assert input2["style_parameters"]["color_scheme"] == "high_contrast"
    assert input2["technical_parameters"]["format"] == "PNG" # Default still applies

    # Test Case 3: Input with data for a chart
    print("\nTest Case 3: Input with data for a chart")
    chart_data = {"labels": ["Jan", "Feb", "Mar"], "values": [10, 20, 15]}
    input3 = process_input(
        "Generate a pie chart showing monthly expenses.",
        content_type="charts",
        data=chart_data,
        data_params={"chart_type": "pie", "data_labels": False},
        technical_params={"dimensions": "800x600", "format": "JPEG"}
    )
    print(json.dumps(input3, indent=2))
    assert input3["content_type"] == "charts"
    assert input3["data"] == chart_data
    assert input3["data_parameters"]["chart_type"] == "pie"
    assert input3["technical_parameters"]["dimensions"] == "800x600"

    # Test Case 4: Invalid content type
    print("\nTest Case 4: Invalid content type")
    try:
        process_input("Some text", content_type="unsupported_type")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        assert "Unsupported content type" in str(e)

    # Test Case 5: Data as JSON string
    print("\nTest Case 5: Data as JSON string")
    json_string_data = '{"categories": ["A", "B"], "counts": [5, 8]}'
    input5 = process_input(
        "Infographic from JSON data.",
        content_type="infographics",
        data=json_string_data
    )
    print(json.dumps(input5, indent=2))
    assert input5["data"] == {"categories": ["A", "B"], "counts": [5, 8]}

    print("\nAll input processing tests passed!")
