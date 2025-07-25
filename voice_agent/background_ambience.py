from pydub import AudioSegment
from .text_to_audio import TextToAudioGenerator

class BackgroundAmbience(TextToAudioGenerator):
    def add_ambience(self, text, voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2", output_path="output_ambience.mp3", ambience_file="news_studio.mp3", speech_volume=0, ambience_volume=-10):
        """
        Generates speech and overlays it on a background ambience track.
        - speech_volume: Volume adjustment for the speech in dB.
        - ambience_volume: Volume adjustment for the ambience in dB.
        """
        try:
            # 1. Generate the speech audio
            speech_path = self.generate_audio(text, voice_id, model_id, "temp_speech.mp3")
            if not speech_path:
                return None

            # 2. Load the speech and ambience audio
            speech = AudioSegment.from_mp3(speech_path)
            ambience = AudioSegment.from_mp3(ambience_file)

            # 3. Adjust volumes
            speech += speech_volume
            ambience += ambience_volume

            # 4. Overlay speech on ambience
            # The speech will be overlaid starting from the beginning of the ambience track.
            final_audio = ambience.overlay(speech)

            # 5. Export the final audio
            final_audio.export(output_path, format="mp3")
            print(f"Audio with ambience saved to {output_path}")
            
            # Clean up temporary speech file
            import os
            os.remove(speech_path)
            
            return output_path
        except FileNotFoundError:
            print(f"Error: Ambience file not found at '{ambience_file}'. Please provide a valid path.")
            return None
        except Exception as e:
            print(f"An error occurred while adding ambience: {e}")
            return None

# Testing code
if __name__ == "__main__":
    ambience_adder = BackgroundAmbience()
    
    # Create a dummy ambience file for testing
    try:
        silence = AudioSegment.silent(duration=10000) # 10 seconds of silence
        silence.export("news_studio.mp3", format="mp3")
        print("Created dummy 'news_studio.mp3' for testing.")
    except Exception as e:
        print(f"Could not create dummy ambience file: {e}")

    # Example: Generate speech with news studio ambience
    print("\nTesting with news studio ambience...")
    ambience_adder.add_ambience(
        "Good evening, and welcome to the nightly news. Our top story tonight: a breakthrough in AI technology.",
        ambience_file="news_studio.mp3",
        output_path="test_news_report.mp3"
    )