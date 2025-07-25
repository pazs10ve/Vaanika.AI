# Kalasetu Voice Agent

This project is a powerful Text-to-Audio generation service built with Python, ElevenLabs API, and FastAPI. It provides a flexible and feature-rich voice agent capable of generating high-quality audio with various customizations.

## Features

- **Text-to-Audio Generation:** Core functionality to convert text into speech using the ElevenLabs API.
- **Context-Aware Voice Modulation:** Adjust the voice's stability and similarity to make it more expressive or stable, depending on the context.
- **Multi-Language and Mixed-Language Support:** 
    - Generate audio in various languages by selecting from a wide range of voices.
    - Handle mixed-language text (e.g., Hinglish) seamlessly with the `eleven_multilingual_v2` model.
- **Background Ambience:** Overlay generated speech with background audio tracks (e.g., a news studio, an open environment) to create more immersive experiences.
- **RESTful API:** All features are exposed through a clean and well-documented FastAPI application.

## Project Structure

```
kalasetu-submission/
├── .env                # For storing API keys
├── app.py              # FastAPI application
├── prompt.txt          # The original prompt for the project
├── README.md           # This file
├── requirements.txt    # Python dependencies
└── voice_agent/
    ├── __init__.py
    ├── background_ambience.py
    ├── language_support.py
    ├── main.py             # Example workflows
    ├── text_to_audio.py
    └── voice_modulation.py
```

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd kalasetu-submission
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    - Rename the `.env.example` file to `.env` (or create a new `.env` file).
    - Add your ElevenLabs API key to the `.env` file:
      ```
      ELEVEN_API_KEY=your_elevenlabs_api_key
      ```

## How to Run

You can interact with the project in two ways:

### 1. Run the Example Workflows

To see a demonstration of all the core features, run the `main.py` script from the root directory. This will generate several example audio files in the `voice_outputs` directory.

```bash
python voice_agent/main.py
```

### 2. Run the FastAPI Server

To use the RESTful API, start the Uvicorn server.

```bash
uvicorn app:app --reload
```

Once the server is running, you can access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

- `POST /generate-audio`: Generates a simple audio file. Also handles mixed-language text.
- `POST /generate-modulated-audio`: Generates audio with custom stability and similarity settings.
- `GET /list-voices`: Lists all available voices from the ElevenLabs API.
- `POST /generate-in-language`: Generates audio in a specific language by finding a voice with matching labels.
- `POST /generate-with-ambience`: Overlays the generated speech with a background audio file.
