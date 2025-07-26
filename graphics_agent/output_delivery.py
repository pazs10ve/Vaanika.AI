import os
import hashlib
from datetime import datetime

def deliver_output(api_response: dict) -> str:
    """
    Extracts and saves the output from the Hugging Face API response.
    Returns the local file path where the image was saved.
    """
    if api_response.get("status") == "completed" and "image_data" in api_response:
        try:
            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            hash_suffix = hashlib.md5(api_response["image_data"]).hexdigest()[:8]
            filename = f"generated_image_{timestamp}_{hash_suffix}.png"
            
            # Create output directory if it doesn't exist
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)
            
            # Full file path
            file_path = os.path.join(output_dir, filename)
            
            # Save the image data
            with open(file_path, "wb") as f:
                f.write(api_response["image_data"])
            
            print(f"✅ Image saved successfully: {file_path}")
            return file_path
            
        except Exception as e:
            return f"Error saving image: {str(e)}"
            
    elif "error" in api_response:
        error_msg = api_response.get("error", "Unknown API error")
        return f"Error: {error_msg}"
    else:
        return "Error: API response did not contain completed status or image data."

def save_image_with_metadata(api_response: dict, prompt: str, technical_params: dict = None) -> str:
    """
    Enhanced version that saves image with metadata file.
    """
    if api_response.get("status") == "completed" and "image_data" in api_response:
        try:
            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            hash_suffix = hashlib.md5(api_response["image_data"]).hexdigest()[:8]
            base_filename = f"generated_image_{timestamp}_{hash_suffix}"
            
            # Create output directory if it doesn't exist
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)
            
            # File paths
            image_path = os.path.join(output_dir, f"{base_filename}.png")
            metadata_path = os.path.join(output_dir, f"{base_filename}_metadata.json")
            
            # Save the image data
            with open(image_path, "wb") as f:
                f.write(api_response["image_data"])
            
            # Save metadata
            metadata = {
                "timestamp": timestamp,
                "prompt": prompt,
                "technical_parameters": technical_params or {},
                "model": "black-forest-labs/FLUX.1-schnell",
                "file_size_bytes": len(api_response["image_data"]),
                "content_type": api_response.get("content_type", "image/png")
            }
            
            import json
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Image saved: {image_path}")
            print(f"✅ Metadata saved: {metadata_path}")
            return image_path
            
        except Exception as e:
            return f"Error saving image with metadata: {str(e)}"
            
    elif "error" in api_response:
        error_msg = api_response.get("error", "Unknown API error")
        return f"Error: {error_msg}"
    else:
        return "Error: API response did not contain completed status or image data."

def display_image_info(file_path: str) -> dict:
    """
    Get information about the saved image file.
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        file_size = os.path.getsize(file_path)
        file_stats = os.stat(file_path)
        creation_time = datetime.fromtimestamp(file_stats.st_ctime)
        
        return {
            "file_path": file_path,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "creation_time": creation_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exists": True
        }
    except Exception as e:
        return {"error": f"Could not get file info: {str(e)}"}

def cleanup_old_images(days_old: int = 7) -> dict:
    """
    Clean up generated images older than specified days.
    """
    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        return {"message": "No images directory found"}
    
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        deleted_count = 0
        total_space_freed = 0
        
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                file_creation_time = os.path.getctime(file_path)
                if file_creation_time < cutoff_time:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    total_space_freed += file_size
        
        return {
            "deleted_files": deleted_count,
            "space_freed_mb": round(total_space_freed / (1024 * 1024), 2),
            "days_old": days_old
        }
    except Exception as e:
        return {"error": f"Cleanup failed: {str(e)}"}

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Output Delivery (Hugging Face Version) ---")

    # Test Case 1: Successful response with mock image data
    print("\nTest Case 1: Successful Response")
    mock_image_data = b'\x89PNG\r\n\x1a\n' + b'mock_image_data' * 100  # Mock PNG data
    success_response = {
        "status": "completed", 
        "image_data": mock_image_data,
        "content_type": "image/png"
    }
    output1 = deliver_output(success_response)
    print(f"Output: {output1}")
    assert not output1.startswith("Error:")
    assert "generated_image_" in output1
    
    # Verify file was actually created
    if os.path.exists(output1):
        print("✅ File created successfully")
        # Get file info
        file_info = display_image_info(output1)
        print(f"File info: {file_info}")
    else:
        print("❌ File was not created")

    # Test Case 2: Error response
    print("\nTest Case 2: Error Response")
    error_response = {"error": "Invalid prompt", "status": "failed"}
    output2 = deliver_output(error_response)
    print(f"Output: {output2}")
    assert "Error: Invalid prompt" in output2

    # Test Case 3: Incomplete response (missing image_data)
    print("\nTest Case 3: Incomplete Response")
    incomplete_response = {"status": "completed"}
    output3 = deliver_output(incomplete_response)
    print(f"Output: {output3}")
    assert "Error: API response did not contain completed status or image data." in output3

    # Test Case 4: Empty response
    print("\nTest Case 4: Empty Response")
    empty_response = {}
    output4 = deliver_output(empty_response)
    print(f"Output: {output4}")
    assert "Error: API response did not contain completed status or image data." in output4

    # Test Case 5: Save with metadata
    print("\nTest Case 5: Save with Metadata")
    test_prompt = "A beautiful landscape painting"
    test_params = {"width": 1024, "height": 576, "guidance_scale": 7.5}
    output5 = save_image_with_metadata(success_response, test_prompt, test_params)
    print(f"Output with metadata: {output5}")
    
    # Check if metadata file exists
    if not output5.startswith("Error:"):
        metadata_file = output5.replace(".png", "_metadata.json")
        if os.path.exists(metadata_file):
            print("✅ Metadata file created successfully")
            import json
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            print(f"Metadata preview: prompt='{metadata.get('prompt')}', model='{metadata.get('model')}'")
        else:
            print("❌ Metadata file was not created")

    # Test Case 6: Cleanup functionality
    print("\nTest Case 6: Cleanup Test")
    cleanup_result = cleanup_old_images(days_old=0)  # Clean all files for testing
    print(f"Cleanup result: {cleanup_result}")

    print("\nAll output delivery tests completed!")
    
    # Show final directory contents
    output_dir = "generated_images"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"\nGenerated images directory contains {len(files)} files:")
        for file in files[:5]:  # Show first 5 files
            print(f"  - {file}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more files")
    else:
        print("\nNo generated images directory found.")