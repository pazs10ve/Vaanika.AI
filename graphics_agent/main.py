from graphics_agent.input_processing import process_input
from graphics_agent.prompt_generation import generate_huggingface_prompt, generate_runway_prompt
from graphics_agent.api_communication import call_huggingface_api, call_runway_api, check_huggingface_setup
from graphics_agent.output_delivery import deliver_output, save_image_with_metadata
import json

def generate_graphic(text_description: str, content_type: str = None, data: dict = None, 
                    style_params: dict = None, technical_params: dict = None, data_params: dict = None,
                    save_metadata: bool = True):
    """
    End-to-end workflow for generating graphics using Hugging Face FLUX model.
    Free alternative to RunwayML with rate limits.
    """
    print(f"\n--- Generating Graphic with Hugging Face: {text_description} ---")
    
    try:
        # 0. Check Hugging Face setup
        setup_check = check_huggingface_setup()
        if setup_check["status"] == "error":
            print(f"❌ Setup Error: {setup_check['message']}")
            for instruction in setup_check.get("setup_instructions", []):
                print(f"   {instruction}")
            return None
        else:
            print(f"✅ {setup_check['message']}")

        # 1. Input Processing
        processed_input = process_input(text_description, content_type, data, style_params, technical_params, data_params)
        print("✅ Input Processed.")

        # 2. Prompt Generation (optimized for FLUX model)
        enhanced_prompt = generate_huggingface_prompt(processed_input)
        print(f"✅ Enhanced Prompt: {enhanced_prompt}")

        # 3. API Communication
        technical_params_for_api = processed_input["technical_parameters"]
        api_response = call_huggingface_api(enhanced_prompt, technical_params_for_api)
        print("✅ API Communication Complete.")

        # 4. Output Delivery
        if save_metadata:
            output_path = save_image_with_metadata(api_response, enhanced_prompt, technical_params_for_api)
        else:
            output_path = deliver_output(api_response)
        
        if not output_path.startswith("Error:"):
            print(f"🎉 Generated Graphic saved at: {output_path}")
            return output_path
        else:
            print(f"❌ {output_path}")
            return None

    except Exception as e:
        print(f"❌ An error occurred during graphic generation: {e}")
        return None

def batch_generate(prompts_list: list, delay_seconds: int = 5):
    """
    Generate multiple graphics with delay to respect rate limits.
    """
    print(f"\n--- Batch Generation: {len(prompts_list)} images with {delay_seconds}s delay ---")
    
    results = []
    for i, prompt_config in enumerate(prompts_list, 1):
        print(f"\n[{i}/{len(prompts_list)}] Processing: {prompt_config.get('text_description', 'Unknown')}")
        
        result = generate_graphic(**prompt_config)
        results.append({
            "config": prompt_config,
            "result": result,
            "success": result is not None and not str(result).startswith("Error:")
        })
        
        # Delay between requests to respect rate limits
        if i < len(prompts_list):
            print(f"⏳ Waiting {delay_seconds} seconds before next generation...")
            import time
            time.sleep(delay_seconds)
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n📊 Batch Summary: {successful}/{len(prompts_list)} successful generations")
    
    return results

def list_supported_features():
    """
    Display supported features and limitations of the Hugging Face version.
    """
    print("\n=== HUGGING FACE VERSION FEATURES ===")
    print("✅ Supported:")
    print("   - Text-to-image generation (FLUX.1-schnell model)")
    print("   - Multiple aspect ratios (1:1, 16:9, 9:16, 4:3)")
    print("   - Custom style parameters")
    print("   - Infographics, charts, illustrations, storyboards")
    print("   - High-quality output (1024px resolution)")
    print("   - Completely FREE with rate limits")
    print("   - Metadata saving")
    print("   - Batch generation with rate limit handling")
    
    print("\n⚠️  Limitations:")
    print("   - Rate limited (free tier)")
    print("   - No video generation (images only)")
    print("   - Cold start delays (model loading)")
    print("   - Max resolution: 1024x1024")
    
    print("\n🔧 Requirements:")
    print("   - Hugging Face account (free)")
    print("   - HF_TOKEN environment variable")
    print("   - Internet connection")
    
    print("\n💡 Tips:")
    print("   - Use descriptive, clear prompts")
    print("   - Wait 5-10 seconds between generations")
    print("   - FLUX.1-schnell is optimized for 4 inference steps")

# --- Example Workflows (Hugging Face Version) ---
if __name__ == "__main__":
    print("--- FREE GRAPHICS GENERATION WITH HUGGING FACE ---")
    list_supported_features()
    
    # Check setup first
    setup_status = check_huggingface_setup()
    if setup_status["status"] == "error":
        print(f"\n❌ Please set up your Hugging Face token first!")
        print("Quick setup guide:")
        for instruction in setup_status.get("setup_instructions", []):
            print(f"   {instruction}")
        exit(1)
    
    print(f"\n✅ Setup Status: {setup_status['message']}")
    
    # Example 1: Business Infographic
    print("\n" + "="*60)
    print("EXAMPLE 1: Business Infographic")
    print("="*60)
    result1 = generate_graphic(
        text_description="Create a quarterly sales performance infographic showing 25% growth.",
        content_type="infographics",
        style_params={"style": "corporate", "color_scheme": "professional"},
        data_params={"data_source": "inline_json"},
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
    
    # Uncomment below for more examples (run one at a time to manage rate limits)
    
    # # Example 2: Data Visualization Chart
    print("\n" + "="*60)
    print("EXAMPLE 2: Data Visualization")
    print("="*60)
    result2 = generate_graphic(
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

    # # Example 3: Mobile Illustration
    print("\n" + "="*60)
    print("EXAMPLE 3: Mobile Illustration")
    print("="*60)
    result3 = generate_graphic(
        text_description="Create a mobile-friendly illustration about our new product launch.",
        content_type="illustrations",
        style_params={"style": "modern", "color_scheme": "vibrant"},
        technical_params={"aspect_ratio": "9:16"}
    )

    # # Example 4: Storyboard
    print("\n" + "="*60)
    print("EXAMPLE 4: Storyboard Layout")
    print("="*60)
    result4 = generate_graphic(
        text_description="Generate a 4-panel storyboard showing customer onboarding process.",
        content_type="storyboards",
        style_params={"tone": "friendly", "complexity": "simple"},
        technical_params={"aspect_ratio": "16:9"}
    )

    # # Example 5: Batch Generation
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Generation")
    print("="*60)
    batch_prompts = [
        {
            "text_description": "A modern office workspace, clean and professional",
            "content_type": "illustrations",
            "style_params": {"style": "modern"},
            "technical_params": {"aspect_ratio": "16:9"}
        },
        {
            "text_description": "A colorful bar chart showing growth metrics",
            "content_type": "charts",
            "style_params": {"color_scheme": "vibrant"},
            "technical_params": {"aspect_ratio": "1:1"}
        }
    ]
    batch_results = batch_generate(batch_prompts, delay_seconds=10)
    
    print("\n" + "="*60)
    print("🎉 GENERATION COMPLETE!")
    print("="*60)
    
    if result1:
        print(f"✅ Your generated graphic is saved at: {result1}")
        print("📁 Check the 'generated_images' folder for all your creations!")
    
    print("\n💡 To generate more images:")
    print("   1. Uncomment other examples in the code")
    print("   2. Run them one at a time to respect rate limits")
    print("   3. Wait 5-10 seconds between generations")
    print("   4. Check your Hugging Face usage at: https://huggingface.co/settings/billing")