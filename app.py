# app.py

import os
import uuid
import logging
import traceback
from fastapi import FastAPI, HTTPException, Request, Depends, status
from pydantic import BaseModel

# --- Local Imports ---
# (Assuming these modules are correctly structured and use the config for API keys)
from voice_agent.voice_modulation import VoiceModulator
from voice_agent.language_support import LanguageSupport
from voice_agent.background_ambience import BackgroundAmbience
from video_agent.video_creation import start_video_generation, check_generation_status
from graphics_agent.main import generate_graphic

# --- Configuration & Logging ---
from config import settings

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
# Add metadata for OpenAPI docs
app = FastAPI(
    title=settings.APP_NAME,
    description="An API for generating voice, video, and graphics.",
    version="1.0.0"
)


# --- API Key Authentication (Placeholder) ---
# In production, you MUST secure your endpoints.
# This is a simple example using a static API key header.
# from fastapi.security import APIKeyHeader
# API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)

# async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
#     if api_key == "YOUR_SECRET_API_KEY": # Replace with a secure key, maybe from settings
#         return api_key
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )

# --- Pydantic Request Models ---
# Models are updated to remove hardcoded defaults where they should be dynamic.

class AudioRequest(BaseModel):
    text: str
    voice_id: str = settings.DEFAULT_VOICE_ID

class ModulatedAudioRequest(AudioRequest):
    stability: float = 0.5
    similarity_boost: float = 0.75

class LanguageAudioRequest(BaseModel):
    text: str
    language_labels: dict

class AmbienceAudioRequest(AudioRequest):
    ambience_file: str # Path to a file accessible by the server
    speech_volume: int = 0
    ambience_volume: int = -10

class VideoGenerationRequest(BaseModel):
    prompt_text: str
    seed: int = None
    duration: int = None
    ratio: str = None
    watermark: bool = None

class GraphicsGenerationRequest(BaseModel):
    text_description: str
    content_type: str = None
    data: dict = None
    style_params: dict = None
    technical_params: dict = None
    data_params: dict = None

# --- Class Instances ---
# In a real app, ensure these classes are initialized with API keys from `settings`
modulator = VoiceModulator()
lang_support = LanguageSupport()
ambience_adder = BackgroundAmbience()


# --- Custom Exception Handler ---
# This prevents leaking internal error details to the client.
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unhandled exception occurred: {exc}\n{traceback.format_exc()}")
    return HTTPException(status_code=500, detail="An internal server error occurred.")

# --- Helper Function for Output Path ---
def get_output_path(extension: str) -> str:
    """Generates a unique output path in the configured directory."""
    return os.path.join(settings.DEFAULT_OUTPUT_DIR, f"{uuid.uuid4()}.{extension}")


# --- API Endpoints ---
# All endpoints are grouped by agent for clarity.
# In a larger app, these would be in separate files under a `routers` directory.

# =================
# Voice Agent
# =================
@app.post("/audio/generate-simple", tags=["Voice Agent"])
async def generate_audio_endpoint(request: AudioRequest):
    output_path = get_output_path("mp3")
    generated_file = modulator.generate_audio(text=request.text, voice_id=request.voice_id, output_path=output_path)
    if generated_file and os.path.exists(generated_file):
        return {"message": "Audio generated successfully", "path": generated_file}
    raise HTTPException(status_code=500, detail="Failed to generate audio.")

@app.get("/audio/list-voices", tags=["Voice Agent"])
async def list_voices_endpoint():
    voices = lang_support.get_available_voices()
    if voices:
        return {"voices": [{"name": v.name, "voice_id": v.voice_id, "labels": v.labels} for v in voices]}
    raise HTTPException(status_code=500, detail="Failed to fetch voices.")

# =================
# Video Agent
# =================
@app.post("/video/generate", tags=["Video Agent"])
async def generate_video_endpoint(request: VideoGenerationRequest):
    runway_options = {
        "seed": request.seed,
        "duration": request.duration,
        "ratio": request.ratio,
        "watermark": request.watermark,
    }
    # Filter out None values to use Runway's defaults
    runway_options = {k: v for k, v in runway_options.items() if v is not None}

    try:
        task = start_video_generation(request.prompt_text, runway_options)
        return {"message": "Video generation initiated.", "task_id": task['uuid']}
    except Exception as e:
        logger.error(f"Failed to start Runway task: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to start video generation task.")

@app.get("/video/status/{task_id}", tags=["Video Agent"])
async def get_video_status_endpoint(task_id: str):
    try:
        task_info = check_generation_status(task_id)
        return task_info
    except Exception as e:
        logger.error(f"Failed to get task status for {task_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to get task status.")

# =================
# Graphics Agent
# =================
@app.post("/graphics/generate", tags=["Graphics Agent"])
async def generate_graphics_endpoint(request: GraphicsGenerationRequest):
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
            return {"message": "Graphics generation successful.", "output_url": output_url}
        else:
            # The function returned a known error string
            logger.error(f"Graphics generation failed with error: {output_url}")
            raise HTTPException(status_code=500, detail=output_url)
    except ValueError as ve:
        # Handle bad input from the user
        logger.warning(f"Invalid input for graphics generation: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Failed to generate graphics: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while generating graphics.")

# --- Main entry point for development ---
if __name__ == "__main__":
    import uvicorn
    print("--- Starting FastAPI server for DEVELOPMENT ---")
    print(f"Access API docs at http://{settings.HOST}:{settings.PORT}/docs")
    # Note: `reload=True` is for development only. Do not use in production.
    # The production server (Gunicorn) will be configured in the Dockerfile.
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)