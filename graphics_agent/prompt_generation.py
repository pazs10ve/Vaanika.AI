def generate_huggingface_prompt(processed_input: dict) -> str:
    """
    Generates an optimized prompt string for the Hugging Face FLUX model based on processed input.
    FLUX models work better with concise, descriptive prompts without technical specifications.
    """
    text_description = processed_input["text_description"]
    content_type = processed_input["content_type"]
    style_params = processed_input["style_parameters"]
    technical_params = processed_input["technical_parameters"]
    data_params = processed_input["data_parameters"]
    data = processed_input["data"]

    prompt_parts = [text_description]

    # Add style parameters in a natural way for FLUX
    style_descriptors = []
    
    # Map style parameters to FLUX-friendly descriptors
    style_map = {
        "modern": "modern, clean, contemporary",
        "corporate": "professional, corporate, business-like",
        "minimalist": "minimalist, simple, clean",
        "artistic": "artistic, creative, expressive",
        "technical": "technical, precise, detailed"
    }
    
    color_scheme_map = {
        "brand_primary": "professional color palette",
        "vibrant": "vibrant colors, bright, energetic",
        "high_contrast": "high contrast, bold colors",
        "monochrome": "monochrome, black and white",
        "pastel": "soft pastel colors",
        "dark": "dark theme, muted colors"
    }
    
    tone_map = {
        "professional": "professional",
        "friendly": "approachable, friendly",
        "serious": "serious, formal",
        "playful": "playful, fun",
        "elegant": "elegant, sophisticated"
    }
    
    complexity_map = {
        "simple": "clean and simple",
        "detailed": "highly detailed",
        "complex": "complex, intricate"
    }

    # Add style descriptors
    if style_params["style"] in style_map:
        style_descriptors.append(style_map[style_params["style"]])
    
    if style_params["color_scheme"] in color_scheme_map:
        style_descriptors.append(color_scheme_map[style_params["color_scheme"]])
    
    if style_params["tone"] in tone_map:
        style_descriptors.append(tone_map[style_params["tone"]])
        
    if style_params["complexity"] in complexity_map:
        style_descriptors.append(complexity_map[style_params["complexity"]])
    
    if style_descriptors:
        prompt_parts.append(", ".join(style_descriptors))

    # Add content-type specific enhancements
    if content_type == "infographics":
        prompt_parts.append("infographic design, data visualization")
        if data:
            # Simplify data representation for FLUX
            data_summary = f"showing data about {', '.join(str(v) for v in data.values() if isinstance(v, (str, int, float)))}"
            prompt_parts.append(data_summary)
        prompt_parts.append("clear layout, visual hierarchy, statistical charts")
        
    elif content_type == "charts":
        chart_type = data_params.get("chart_type", "chart")
        prompt_parts.append(f"{chart_type} chart, data visualization")
        if data:
            # Extract key info from data for the prompt
            if "labels" in data and "values" in data:
                prompt_parts.append(f"with {len(data['labels'])} categories")
        prompt_parts.append("clean typography, professional chart design")
        
    elif content_type == "illustrations":
        prompt_parts.append("detailed illustration, high quality artwork")
        
    elif content_type == "storyboards":
        prompt_parts.append("storyboard layout, sequential panels, narrative flow")
        prompt_parts.append("multiple scenes, visual storytelling")

    # Add quality enhancers for FLUX
    quality_enhancers = [
        "high quality",
        "professional design",
        "sharp details"
    ]
    
    # Add aspect ratio hint (FLUX doesn't use technical specs but benefits from composition hints)
    aspect_ratio = technical_params.get("aspect_ratio", "1:1")
    if aspect_ratio in ["16:9", "landscape"]:
        quality_enhancers.append("wide composition")
    elif aspect_ratio in ["9:16", "portrait"]:
        quality_enhancers.append("vertical composition")
    elif aspect_ratio in ["1:1", "square"]:
        quality_enhancers.append("square composition")

    prompt_parts.extend(quality_enhancers)

    # Join all parts and clean up
    final_prompt = ", ".join(prompt_parts)
    
    # Clean up any double commas or spaces
    final_prompt = final_prompt.replace(", ,", ",").replace("  ", " ").strip()
    
    return final_prompt

# Backward compatibility - keep the old function name
def generate_runway_prompt(processed_input: dict) -> str:
    """
    Backward compatibility wrapper for generate_huggingface_prompt.
    """
    return generate_huggingface_prompt(processed_input)

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Prompt Generation (Hugging Face Version) ---")

    # Mock processed_input structure
    def mock_process_input(text_description, content_type=None, data=None, style_params=None, technical_params=None, data_params=None):
        from input_processing import process_input
        return process_input(text_description, content_type, data, style_params, technical_params, data_params)

    # Test Case 1: Basic illustration prompt
    print("\nTest Case 1: Basic illustration prompt")
    input1 = mock_process_input("A futuristic city skyline at sunset.", content_type="illustrations")
    prompt1 = generate_huggingface_prompt(input1)
    print(f"Generated Prompt:\n{prompt1}")
    assert "A futuristic city skyline at sunset" in prompt1
    assert "modern, clean, contemporary" in prompt1
    assert "detailed illustration" in prompt1

    # Test Case 2: Infographic prompt with data
    print("\nTest Case 2: Infographic prompt with data")
    data_for_info = {"title": "Sales Growth", "Q1": "10%", "Q2": "15%"}
    input2 = mock_process_input(
        "Infographic showing quarterly sales growth.",
        content_type="infographics",
        data=data_for_info,
        style_params={"style": "corporate", "color_scheme": "vibrant"},
        technical_params={"aspect_ratio": "16:9"}
    )
    prompt2 = generate_huggingface_prompt(input2)
    print(f"Generated Prompt:\n{prompt2}")
    assert "Infographic showing quarterly sales growth" in prompt2
    assert "professional, corporate, business-like" in prompt2
    assert "vibrant colors" in prompt2
    assert "infographic design" in prompt2
    assert "wide composition" in prompt2

    # Test Case 3: Chart prompt with specific parameters
    print("\nTest Case 3: Chart prompt with specific parameters")
    chart_data = {"labels": ["A", "B", "C"], "values": [30, 50, 20]}
    input3 = mock_process_input(
        "Pie chart of market share.",
        content_type="charts",
        data=chart_data,
        style_params={"tone": "professional", "complexity": "detailed"},
        data_params={"chart_type": "pie", "data_labels": True, "legend_position": "right"},
        technical_params={"aspect_ratio": "1:1"}
    )
    prompt3 = generate_huggingface_prompt(input3)
    print(f"Generated Prompt:\n{prompt3}")
    assert "Pie chart of market share" in prompt3
    assert "pie chart, data visualization" in prompt3
    assert "with 3 categories" in prompt3
    assert "highly detailed" in prompt3
    assert "square composition" in prompt3

    # Test Case 4: Storyboard prompt
    print("\nTest Case 4: Storyboard prompt")
    input4 = mock_process_input(
        "A 3-panel storyboard of a user signing up.", 
        content_type="storyboards",
        technical_params={"aspect_ratio": "16:9"}
    )
    prompt4 = generate_huggingface_prompt(input4)
    print(f"Generated Prompt:\n{prompt4}")
    assert "A 3-panel storyboard of a user signing up" in prompt4
    assert "storyboard layout" in prompt4
    assert "sequential panels" in prompt4
    assert "wide composition" in prompt4

    # Test Case 5: Portrait mobile design
    print("\nTest Case 5: Portrait mobile design")
    input5 = mock_process_input(
        "Mobile app interface design.",
        content_type="illustrations",
        style_params={"style": "modern", "color_scheme": "dark"},
        technical_params={"aspect_ratio": "9:16"}
    )
    prompt5 = generate_huggingface_prompt(input5)
    print(f"Generated Prompt:\n{prompt5}")
    assert "Mobile app interface design" in prompt5
    assert "dark theme" in prompt5
    assert "vertical composition" in prompt5

    print("\nAll prompt generation tests passed!")