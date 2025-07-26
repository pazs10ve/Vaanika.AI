"""
This file contains functions for applying enhancements to the video generation process.
For Runway ML, these are typically passed as parameters in the initial generation call.
"""

def set_ratio(ratio="16:9"):
    """
    Sets the aspect ratio of the output video.

    Args:
        ratio (str): The aspect ratio, e.g., "16:9", "9:16", "1:1".

    Returns:
        dict: A dictionary containing the ratio parameter.
    """
    return {"ratio": ratio}

def enable_watermark(enabled=False):
    """
    Specifies whether to include a watermark on the video.

    Args:
        enabled (bool): False to disable the default watermark.

    Returns:
        dict: A dictionary containing the watermark setting.
    """
    return {"watermark": enabled}

if __name__ == "__main__":
    # Test ratio setting
    ratio = set_ratio("1:1")
    print(f"Ratio parameter: {ratio}")

    # Test watermark setting
    watermark = enable_watermark(False)
    print(f"Watermark parameter: {watermark}")