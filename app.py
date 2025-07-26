from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from voice_agent.voice_modulation import VoiceModulator
from voice_agent.language_support import LanguageSupport
from voice_agent.background_ambience import BackgroundAmbience
from video_agent.video_creation import start_video_generation, check_generation_status
import os
from graphics_agent.input_processing import process_input
from graphics_agent.prompt_generation import generate_runway_prompt
from graphics_agent.api_communication import call_runway_api
from graphics_agent.output_delivery import deliver_output
from graphics_agent.main import generate_graphic

import os


app = FastAPI()


# --- Voice Agent Request Models ---
class AudioRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    output_path: str = "api_output.mp3"

class ModulatedAudioRequest(AudioRequest):
    stability: float = 0.5
    similarity_boost: float = 0.75

class LanguageAudioRequest(BaseModel):
    text: str
    language_labels: dict
    output_path: str = "api_language_output.mp3"

class AmbienceAudioRequest(AudioRequest):
    ambience_file: str
    speech_volume: int = 0
    ambience_volume: int = -10

# --- Video Agent Request Models ---
class VideoGenerationRequest(BaseModel):
    prompt_text: str
    seed: int = None
    duration: int = None
    ratio: str = None
    watermark: bool = None

# --- Graphics Agent Request Models ---
class GraphicsGenerationRequest(BaseModel):
    text_description: str
    content_type: str = None
    data: dict = None
    style_params: dict = None
    technical_params: dict = None
    data_params: dict = None

# --- Instances of our classes ---
modulator = VoiceModulator()
lang_support = LanguageSupport()
ambience_adder = BackgroundAmbience()

# --- Voice Agent API Endpoints ---

@app.post("/audio/generate-simple")
async def generate_audio_endpoint(request: AudioRequest):
    output_path = modulator.generate_audio(text=request.text, voice_id=request.voice_id, output_path=request.output_path)
    if output_path and os.path.exists(output_path):
        return {"message": "Audio generated successfully", "path": output_path}
    raise HTTPException(status_code=500, detail="Failed to generate audio.")

@app.post("/audio/generate-modulated")
async def generate_modulated_audio_endpoint(request: ModulatedAudioRequest):
    output_path = modulator.generate_with_modulation(text=request.text, voice_id=request.voice_id, output_path=request.output_path, stability=request.stability, similarity_boost=request.similarity_boost)
    if output_path and os.path.exists(output_path):
        return {"message": "Modulated audio generated successfully", "path": output_path}
    raise HTTPException(status_code=500, detail="Failed to generate modulated audio.")

@app.get("/audio/list-voices")
async def list_voices_endpoint():
    voices = lang_support.get_available_voices()
    if voices:
        return {"voices": [{"name": v.name, "voice_id": v.voice_id, "labels": v.labels} for v in voices]}
    raise HTTPException(status_code=500, detail="Failed to fetch voices.")

@app.post("/audio/generate-in-language")
async def generate_in_language_endpoint(request: LanguageAudioRequest):
    output_path = lang_support.generate_in_language(text=request.text, language_labels=request.language_labels, output_path=request.output_path)
    if output_path and os.path.exists(output_path):
        return {"message": f"Audio in language '{request.language_labels}' generated successfully", "path": output_path}
    raise HTTPException(status_code=500, detail=f"Could not find a voice for the labels: {request.language_labels}")

@app.post("/audio/generate-with-ambience")
async def generate_with_ambience_endpoint(request: AmbienceAudioRequest):
    if not os.path.exists(request.ambience_file):
        raise HTTPException(status_code=404, detail=f"Ambience file not found: {request.ambience_file}")
    output_path = ambience_adder.add_ambience(text=request.text, voice_id=request.voice_id, output_path=request.output_path, ambience_file=request.ambience_file, speech_volume=request.speech_volume, ambience_volume=request.ambience_volume)
    if output_path and os.path.exists(output_path):
        return {"message": "Audio with ambience generated successfully", "path": output_path}
    raise HTTPException(status_code=500, detail="Failed to generate audio with ambience.")

# --- Video Agent API Endpoints (Runway ML SDK) ---

@app.post("/video/generate")
async def generate_video_endpoint(request: VideoGenerationRequest):
    """
    Starts a video generation task.
    """
    options = {
        "seed": request.seed,
        "duration": request.duration,
        "ratio": request.ratio,
        "watermark": request.watermark,
    }
    runway_options = {k: v for k, v in options.items() if v is not None}

    try:
        task = start_video_generation(request.prompt_text, runway_options)
        return {"message": "Video generation initiated.", "task_id": task['uuid']}
    except Exception as e:
        import traceback
        print("--- DETAILED ERROR TRACEBACK ---")
        traceback.print_exc()
        print("---------------------------------")
        raise HTTPException(status_code=500, detail=f"Failed to start Runway task: {e}")

@app.get("/video/status/{task_id}")
async def get_video_status_endpoint(task_id: str):
    """
    Checks the status of a video generation task using its ID.
    """
    try:
        # Get the task object by its ID
        task_info = check_generation_status(task_id)
        return task_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {e}")

# --- Graphics Agent API Endpoints ---

@app.post("/graphics/generate")
async def generate_graphics_endpoint(request: GraphicsGenerationRequest):
    """
    Generates graphics based on text description and parameters using RunwayML.
    """
    try:
        output_url = generate_graphic(
            text_description=request.text_description,
            content_type=request.content_type,
            data=request.data,
            style_params=request.style_params,
            technical_params=request.technical_params,
            data_params=request.data_params
        )
        if output_url and not output_url.startswith("Error:"):
            return {"message": "Graphics generation initiated/completed.", "output_url": output_url}
        else:
            raise HTTPException(status_code=500, detail=output_url)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        print("--- DETAILED ERROR TRACEBACK ---")
        traceback.print_exc()
        print("---------------------------------")
        raise HTTPException(status_code=500, detail=f"Failed to generate graphics: {e}")


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server. Access the API docs at http://127.0.0.1:8000/docs")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
