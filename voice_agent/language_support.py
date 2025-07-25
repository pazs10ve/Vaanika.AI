from .text_to_audio import TextToAudioGenerator

class LanguageSupport(TextToAudioGenerator):
    def get_available_voices(self):
        """
        Retrieves and prints information about all available voices.
        """
        try:
            voices = self.client.voices.get_all()
            for voice in voices.voices:
                print(f"Name: {voice.name}, Voice ID: {voice.voice_id}")
                if voice.labels:
                    print(f"  Labels: {voice.labels}")
            return voices.voices
        except Exception as e:
            print(f"An error occurred while fetching voices: {e}")
            return None

    def generate_in_language(self, text, language_labels, output_path="output_language.mp3"):
        """
        Generates audio in a specific language by finding a suitable voice.
        """
        try:
            voices = self.client.voices.get_all().voices
            # Find a voice that matches the desired language labels
            voice_id = None
            for voice in voices:
                if voice.labels and all(label in voice.labels for label in language_labels):
                    voice_id = voice.voice_id
                    print(f"Found voice '{voice.name}' for language labels: {language_labels}")
                    break
            
            if voice_id:
                return self.generate_audio(text, voice_id=voice_id, output_path=output_path)
            else:
                print(f"No voice found for the specified language labels: {language_labels}")
                return None
        except Exception as e:
            print(f"An error occurred during language generation: {e}")
            return None

# Testing code
if __name__ == "__main__":
    lang_support = LanguageSupport()
    
    # Example 1: List all available voices
    print("Fetching all available voices...")
    lang_support.get_available_voices()
    
    # Example 2: Generate audio in Spanish (example)
    # Note: This requires a voice with 'spanish' and 'accent' labels in your ElevenLabs account.
    # You may need to adjust the labels based on the voices available to you.
    print("\nTesting with a Spanish voice...")
    lang_support.generate_in_language(
        "Hola, ¿cómo estás?",
        language_labels={'accent': 'spanish', 'use case': 'narration'},
        output_path="test_spanish.mp3"
    )