def deliver_output(api_response: dict) -> str:
    """
    Extracts and returns the output URL from the RunwayML API response.
    """
    if api_response.get("status") == "completed" and "output_url" in api_response:
        return api_response["output_url"]
    elif "error" in api_response:
        return f"Error: {api_response.get("error", "Unknown API error")}"
    else:
        return "Error: API response did not contain a completed status or output URL."

# --- Testing Code ---
if __name__ == "__main__":
    print("--- Testing Output Delivery ---")

    # Test Case 1: Successful response
    print("\nTest Case 1: Successful Response")
    success_response = {"id": "img_123", "status": "completed", "output_url": "https://example.com/image.png"}
    output1 = deliver_output(success_response)
    print(f"Output: {output1}")
    assert output1 == "https://example.com/image.png"

    # Test Case 2: Error response
    print("\nTest Case 2: Error Response")
    error_response = {"error": "Invalid prompt", "status": "failed"}
    output2 = deliver_output(error_response)
    print(f"Output: {output2}")
    assert "Error: Invalid prompt" in output2

    # Test Case 3: Incomplete response (missing output_url)
    print("\nTest Case 3: Incomplete Response")
    incomplete_response = {"id": "img_456", "status": "completed"}
    output3 = deliver_output(incomplete_response)
    print(f"Output: {output3}")
    assert "Error: API response did not contain a completed status or output URL." in output3

    # Test Case 4: Empty response
    print("\nTest Case 4: Empty Response")
    empty_response = {}
    output4 = deliver_output(empty_response)
    print(f"Output: {output4}")
    assert "Error: API response did not contain a completed status or output URL." in output4

    print("\nAll output delivery tests passed!")
