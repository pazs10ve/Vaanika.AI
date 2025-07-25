from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from voice_agent.voice_modulation import VoiceModulator
from voice_agent.language_support import LanguageSupport
from voice_agent.background_ambience import BackgroundAmbience
import os

app = FastAPI()

# --- Request Models ---
class AudioRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM" # Default to Rachel
    output_path: str = "api_output.mp3"

class ModulatedAudioRequest(AudioRequest):
    stability: float = 0.5
    similarity_boost: float = 0.75

class LanguageAudioRequest(BaseModel):
    text: str
    # The labels to identify the desired language and accent.
    # Example: {"accent": "spanish", "use case": "narration"}
    language_labels: dict
    output_path: str = "api_language_output.mp3"

class AmbienceAudioRequest(AudioRequest):
    ambience_file: str
    speech_volume: int = 0
    ambience_volume: int = -10

# --- Instances of our classes ---
modulator = VoiceModulator()
lang_support = LanguageSupport()
ambience_adder = BackgroundAmbience()

# --- API Endpoints ---

@app.post("/generate-audio")
async def generate_audio_endpoint(request: AudioRequest):
    """
    Generates a simple audio file from text. Also suitable for mixed-language (e.g., Hinglish) text.
    """
    output_path = modulator.generate_audio(
        text=request.text,
        voice_id=request.voice_id,
        model_id="eleven_multilingual_v2", # Ensure multilingual model is used
        output_path=request.output_path
    )
    if output_path and os.path.exists(output_path):
        return {"message": "Audio generated successfully", "path": output_path}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio.")

@app.post("/generate-modulated-audio")
async def generate_modulated_audio_endpoint(request: ModulatedAudioRequest):
    """
    Generates audio with specific voice modulation settings.
    """
    output_path = modulator.generate_with_modulation(
        text=request.text,
        voice_id=request.voice_id,
        output_path=request.output_path,
        stability=request.stability,
        similarity_boost=request.similarity_boost
    )
    if output_path and os.path.exists(output_path):
        return {"message": "Modulated audio generated successfully", "path": output_path}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate modulated audio.")

@app.get("/list-voices")
async def list_voices_endpoint():
    """
    Lists all available voices from the ElevenLabs API.
    """
    voices = lang_support.get_available_voices()
    if voices:
        return {"voices": [{"name": v.name, "voice_id": v.voice_id, "labels": v.labels} for v in voices]}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch voices.")

@app.post("/generate-in-language")
async def generate_in_language_endpoint(request: LanguageAudioRequest):
    """
    Generates audio in a specific language by finding a voice with matching labels.
    """
    output_path = lang_support.generate_in_language(
        text=request.text,
        language_labels=request.language_labels,
        output_path=request.output_path
    )
    if output_path and os.path.exists(output_path):
        return {"message": f"Audio in language '{request.language_labels}' generated successfully", "path": output_path}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to generate audio. Could not find a voice for the labels: {request.language_labels}")

@app.post("/generate-with-ambience")
async def generate_with_ambience_endpoint(request: AmbienceAudioRequest):
    """
    Generates speech and overlays it on a background ambience track.
    """
    if not os.path.exists(request.ambience_file):
        raise HTTPException(status_code=404, detail=f"Ambience file not found: {request.ambience_file}")

    output_path = ambience_adder.add_ambience(
        text=request.text,
        voice_id=request.voice_id,
        output_path=request.output_path,
        ambience_file=request.ambience_file,
        speech_volume=request.speech_volume,
        ambience_volume=request.ambience_volume
    )
    if output_path and os.path.exists(output_path):
        return {"message": "Audio with ambience generated successfully", "path": output_path}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio with ambience.")

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server. Access the API at http://127.0.0.1:8000/docs")
    # To run: uvicorn app:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
