from .voice_modulation import VoiceModulator
from .language_support import LanguageSupport
from .background_ambience import BackgroundAmbience

def run_example_workflows():
    """
    Demonstrates various workflows using the voice agent modules.
    """
    print("--- Running Example Workflows ---")

    # Workflow 1: Generate a simple audio file with a specific voice
    print("\n--- Workflow 1: Simple Text-to-Audio ---")
    modulator = VoiceModulator()
    modulator.generate_audio(
        text="This is a standard audio generation test.",
        voice_id="21m00Tcm4TlvDq8ikWAM", # Rachel
        output_path="workflow_1_simple.mp3"
    )

    # Workflow 2: Generate an expressive audio file
    print("\n--- Workflow 2: Expressive Voice Modulation ---")
    modulator.generate_with_modulation(
        text="Wow, this is truly amazing! I can't believe it.",
        voice_id="21m00Tcm4TlvDq8ikWAM", # Rachel
        output_path="workflow_2_expressive.mp3",
        stability=0.4,
        similarity_boost=0.7
    )

    # Workflow 3: Generate audio in a different language (e.g., German)
    # This requires a voice with the appropriate language labels.
    print("\n--- Workflow 3: Multi-language Generation ---")
    lang_support = LanguageSupport()
    lang_support.generate_in_language(
        text="Hallo, wie geht es Ihnen heute?",
        language_labels={'accent': 'german'},
        output_path="workflow_3_german.mp3"
    )

    # Workflow 4: Generate a news report with background ambience
    print("\n--- Workflow 4: News Report with Ambience ---")
    # Create a dummy ambience file if it doesn't exist
    try:
        from pydub import AudioSegment
        import os
        if not os.path.exists("news_studio.mp3"):
            silence = AudioSegment.silent(duration=15000) # 15 seconds
            silence.export("news_studio.mp3", format="mp3")
            print("Created dummy 'news_studio.mp3' for ambience.")
    except Exception as e:
        print(f"Could not create dummy ambience file: {e}")
        
    ambience_adder = BackgroundAmbience()
    ambience_adder.add_ambience(
        text="In world news today, diplomats from several nations gathered to discuss the future of space exploration.",
        voice_id="21m00Tcm4TlvDq8ikWAM", # Rachel
        ambience_file="news_studio.mp3",
        output_path="workflow_4_news_report.mp3"
    )

    # Workflow 5: Generate mixed-language (Hinglish) audio
    print("\n--- Workflow 5: Mixed-Language (Hinglish) Generation ---")
    modulator.generate_audio(
        text="That's a great idea, chalo karte hain!",
        voice_id="21m00Tcm4TlvDq8ikWAM", # Using a versatile voice
        model_id="eleven_multilingual_v2", # Ensure the multilingual model is used
        output_path="workflow_5_hinglish.mp3"
    )

    print("\n--- Example Workflows Complete ---")

if __name__ == "__main__":
    run_example_workflows()