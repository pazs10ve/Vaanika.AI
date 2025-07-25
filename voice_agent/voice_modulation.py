from voice_agent.text_to_audio import TextToAudioGenerator

class VoiceModulator(TextToAudioGenerator):
    def generate_with_modulation(self, text, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2", output_path="output_modulated.mp3", stability=0.5, similarity_boost=0.75):
        """
        Generates audio with specific voice modulation settings.
        - stability: Higher values make the voice more stable, but less expressive.
        - similarity_boost: Higher values make the voice more similar to the original, but can introduce artifacts.
        """
        try:
            print(f"Generating audio with stability={stability} and similarity_boost={similarity_boost}")
            
            audio_stream = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                voice_settings={
                    "stability": stability,
                    "similarity_boost": similarity_boost
                }
            )

            with open(output_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)
            
            print(f"Audio generated and saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"An error occurred during modulation: {e}")
            return None

# Testing code
if __name__ == "__main__":
    modulator = VoiceModulator()
    
    # Example 1: More expressive voice
    print("Testing with a more expressive voice (low stability)...")
    modulator.generate_with_modulation(
        "I am so excited to try this!",
        output_path="test_expressive.mp3",
        stability=0.3,
        similarity_boost=0.75
    )
    
    # Example 2: More stable (robotic) voice
    print("\nTesting with a more stable voice (high stability)...")
    modulator.generate_with_modulation(
        "This is a very serious announcement.",
        output_path="test_stable.mp3",
        stability=0.9,
        similarity_boost=0.75
    )
