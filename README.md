# Kalasetu Voice & Video Agent

"Vaanika.AI is a full-stack multimodal AI studio that empowers creators to create and narrate stories that inspire. 

### Voice Agent
- **Text-to-Audio Generation:** Convert text into speech using the ElevenLabs API.
- **Context-Aware Voice Modulation:** Adjust voice stability and similarity.
- **Multi-Language Support:** Generate audio in various languages and handle mixed-language text.
- **Background Ambience:** Overlay speech with background audio.

### Video Agent
- **Text-to-Video Generation:** Convert a script into a video with an AI avatar.
- **Customization:**
    - **Avatar/Model:** Choose the AI model for narration.
    - **Background:** Set a solid color or an image URL as the background.
    - **Subtitles:** Automatically include subtitles.
    - **Background Music:** Add background music from a URL.

## Project Structure
```
kalasetu-submission/
├── .env
├── app.py              # FastAPI application
├── prompt.txt
├── README.md
├── requirements.txt
├── voice_agent/        # Voice generation modules
└── video_agent/        # Video generation modules
```

## Setup and Installation

1.  **Clone the repository.**
2.  **Create and activate a virtual environment.**
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Set up API keys in a `.env` file:**
    ```
    ELEVEN_API_KEY=your_elevenlabs_api_key
    DEEPBRAIN_API_KEY=your_deepbrain_api_key
    ```

## How to Run

### 1. Run Example Workflows

- **Voice Agent:** `python -m voice_agent.main`
- **Video Agent:** `python -m video_agent.main`

### 2. Run the FastAPI Server

```bash
uvicorn app:app --reload
```
Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

### Voice Agent
- `POST /audio/generate-simple`
- `POST /audio/generate-modulated`
- `GET /audio/list-voices`
- `POST /audio/generate-in-language`
- `POST /audio/generate-with-ambience`

### Video Agent
- `POST /video/generate-custom`: Creates a video with options for title, model, background, subtitles, and music.

---

### Video Agent - Known Issues

**API Key Permissions:** The Deep Brain AI API key used for development has "Insufficient permissions" (Error Code 2004) for video creation. The implemented code is based on the official API documentation and is expected to work with a fully permissioned API key. To test the video generation functionality, please replace the key in the `.env` file with one that has the necessary rights.
