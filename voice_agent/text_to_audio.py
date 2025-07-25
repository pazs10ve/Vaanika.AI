import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

class TextToAudioGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("ELEVEN_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the ELEVEN_API_KEY environment variable.")
        self.client = ElevenLabs(api_key=api_key)

    def generate_audio(self, text, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2", output_path="output_audio.mp3"):
        """
        Generates audio from text using the ElevenLabs API and saves it to a file.
        """
        try:
            audio_stream = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id
            )

            with open(output_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)
            
            print(f"Audio generated and saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Testing code
if __name__ == "__main__":
    generator = TextToAudioGenerator()
    
    # Example 1: Default voice
    print("Testing with default voice...")
    generator.generate_audio("Hello, this is a test of the default voice.", output_path="test_default.mp3")
    
    # Example 2: A different voice (example ID, may need to be changed)
    print("\nTesting with a different voice...")
    generator.generate_audio("This is a different voice.", voice_id="21m00Tcm4TlvDq8ikWAM", output_path="test_different_voice.mp3")
