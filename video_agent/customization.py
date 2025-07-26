"""
This file contains functions for applying customizations to the video generation process.
For Runway ML, these are typically passed as parameters in the initial generation call.
"""

def set_seed(seed_value=None):
    """
    Sets a seed for reproducible generation.

    Args:
        seed_value (int, optional): The seed value. Defaults to None (random).

    Returns:
        dict: A dictionary containing the seed parameter if provided.
    """
    if seed_value is not None:
        return {"seed": seed_value}
    return {}

def set_duration(seconds=5):
    """
    Sets the duration of the generated video in seconds.

    Args:
        seconds (int): The duration in seconds (e.g., 5 or 10).

    Returns:
        dict: A dictionary containing the duration parameter.
    """
    return {"duration": seconds}

if __name__ == "__main__":
    # Test seed setting
    seed = set_seed(42)
    print(f"Seed parameter: {seed}")

    no_seed = set_seed()
    print(f"Seed parameter (default): {no_seed}")

    # Test duration setting
    duration = set_duration(10)
    print(f"Duration parameter: {duration}")