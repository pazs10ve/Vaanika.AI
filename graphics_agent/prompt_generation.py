def generate_runway_prompt(processed_input: dict) -> str:
    """
    Generates an optimized prompt string for the RunwayML API based on processed input.
    """
    text_description = processed_input["text_description"]
    content_type = processed_input["content_type"]
    style_params = processed_input["style_parameters"]
    technical_params = processed_input["technical_parameters"]
    data_params = processed_input["data_parameters"]
    data = processed_input["data"]

    prompt_parts = [text_description]

    # Inject style parameters
    style_str = f"style: {style_params["style"]}, color scheme: {style_params["color_scheme"]}, tone: {style_params["tone"]}, complexity: {style_params["complexity"]}."
    prompt_parts.append(style_str)

    # Add content-type specific phrasing and data integration
    if content_type == "infographics":
        prompt_parts.append("Create a data-driven infographic.")
        if data:
            prompt_parts.append(f"Visualize the following data: {data}")
        prompt_parts.append("Ensure clear visual hierarchy and statistical representation.")
    elif content_type == "charts":
        chart_type = data_params.get("chart_type", "chart")
        data_labels = "with data labels" if data_params.get("data_labels") else "without data labels"
        legend_position = f"legend at {data_params.get("legend_position")}" if data_params.get("legend_position") != "none" else "no legend"
        prompt_parts.append(f"Generate a {chart_type} chart {data_labels} and {legend_position}.")
        if data:
            prompt_parts.append(f"Display the following data: {data}")
        prompt_parts.append("Use clean typography.")
    elif content_type == "illustrations":
        prompt_parts.append("Generate a detailed illustration.")
    elif content_type == "storyboards":
        prompt_parts.append("Create a sequential visual narrative storyboard.")
        prompt_parts.append("Consider multi-panel layouts and character-based scenes if applicable.")

    # Add technical quality descriptors
    tech_str = (
        f"Dimensions: {technical_params["dimensions"]}, "
        f"format: {technical_params["format"]}, "
        f"resolution: {technical_params["resolution"]}, "
        f"aspect ratio: {technical_params["aspect_ratio"]}. "
        "Ensure high quality, professional design."
    )
    prompt_parts.append(tech_str)

    # Join all parts to form the final prompt
    return " ".join(prompt_parts).strip()

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Prompt Generation ---")

    # Mock processed_input from input_processing.py
    from .input_processing import process_input

    # Test Case 1: Basic illustration prompt
    print("\nTest Case 1: Basic illustration prompt")
    input1 = process_input("A futuristic city skyline at sunset.", content_type="illustrations")
    prompt1 = generate_runway_prompt(input1)
    print(f"Generated Prompt:\n{prompt1}")
    assert "A futuristic city skyline at sunset." in prompt1
    assert "style: modern" in prompt1
    assert "Generate a detailed illustration." in prompt1

    # Test Case 2: Infographic prompt with data
    print("\nTest Case 2: Infographic prompt with data")
    data_for_info = {"title": "Sales Growth", "Q1": "10%", "Q2": "15%"}
    input2 = process_input(
        "Infographic showing quarterly sales growth.",
        content_type="infographics",
        data=data_for_info,
        style_params={"style": "corporate", "color_scheme": "vibrant"},
        technical_params={"dimensions": "1920x1080", "format": "JPEG"}
    )
    prompt2 = generate_runway_prompt(input2)
    print(f"Generated Prompt:\n{prompt2}")
    assert "Infographic showing quarterly sales growth." in prompt2
    assert "style: corporate" in prompt2
    assert "Visualize the following data:" in prompt2
    assert "Dimensions: 1920x1080" in prompt2

    # Test Case 3: Chart prompt with specific parameters
    print("\nTest Case 3: Chart prompt with specific parameters")
    chart_data = {"labels": ["A", "B", "C"], "values": [30, 50, 20]}
    input3 = process_input(
        "Pie chart of market share.",
        content_type="charts",
        data=chart_data,
        style_params={"tone": "professional", "complexity": "detailed"},
        data_params={"chart_type": "pie", "data_labels": True, "legend_position": "right"},
        technical_params={"resolution": "print_quality", "aspect_ratio": "4:3"}
    )
    prompt3 = generate_runway_prompt(input3)
    print(f"Generated Prompt:\n{prompt3}")
    assert "Pie chart of market share." in prompt3
    assert "Generate a pie chart with data labels and legend at right." in prompt3
    assert "Display the following data:" in prompt3
    assert "resolution: print_quality" in prompt3

    # Test Case 4: Storyboard prompt
    print("\nTest Case 4: Storyboard prompt")
    input4 = process_input("A 3-panel storyboard of a user signing up.", content_type="storyboards")
    prompt4 = generate_runway_prompt(input4)
    print(f"Generated Prompt:\n{prompt4}")
    assert "A 3-panel storyboard of a user signing up." in prompt4
    assert "Create a sequential visual narrative storyboard." in prompt4

    print("\nAll prompt generation tests passed!")
