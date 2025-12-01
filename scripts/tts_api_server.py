#!/usr/bin/env python3
"""
OpenAI-compatible TTS API Server
Provides local TTS service without API key requirements

Usage:
    python3 scripts/tts_api_server.py
    # Server runs on http://localhost:8000
"""

import asyncio
import io
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("❌ Required packages not installed")
    print("   Install with: pip install fastapi uvicorn")
    sys.exit(1)

try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  TTS library not available, will use fallback")


app = FastAPI(title="OpenAI-Compatible TTS API")


class SpeechRequest(BaseModel):
    model: str = "gpt-4o-mini-tts"
    voice: str = "onyx"
    input: str
    instructions: Optional[str] = None
    response_format: str = "pcm"


# Voice mapping (onyx = deep male voice)
VOICE_MODELS = {
    "onyx": "tts_models/en/ljspeech/tacotron2-DDC",  # Deep, dramatic
    "alloy": "tts_models/en/ljspeech/tacotron2-DDC",
    "echo": "tts_models/en/ljspeech/tacotron2-DDC",
    "fable": "tts_models/en/ljspeech/tacotron2-DDC",
    "nova": "tts_models/en/ljspeech/tacotron2-DDC",
    "shimmer": "tts_models/en/ljspeech/tacotron2-DDC",
    "coral": "tts_models/en/ljspeech/tacotron2-DDC",
}


def get_tts_model(voice: str = "onyx"):
    """Get TTS model for voice"""
    if not TTS_AVAILABLE:
        return None
    
    model_name = VOICE_MODELS.get(voice, VOICE_MODELS["onyx"])
    try:
        return TTS(model_name=model_name)
    except Exception as e:
        print(f"⚠️  Error loading TTS model: {e}")
        return None


async def generate_speech_stream(text: str, voice: str = "onyx"):
    """Generate speech and stream as PCM audio"""
    # Try TTS first, fallback to simple synthesis if not available
    if TTS_AVAILABLE:
        tts = get_tts_model(voice)
        if tts:
            # Generate to temporary WAV file
            import tempfile
            import wave
            import numpy as np
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_path = tmp_file.name
            
            try:
                # Generate speech
                tts.tts_to_file(text=text, file_path=temp_path)
                
                # Read WAV and convert to PCM (16-bit, 24kHz, mono)
                with wave.open(temp_path, 'rb') as wav_file:
                    frames = wav_file.readframes(wav_file.getnframes())
                    sample_rate = wav_file.getframerate()
                    
                    # Convert to 16-bit PCM
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                    
                    # Resample to 24kHz if needed (OpenAI TTS uses 24kHz)
                    if sample_rate != 24000:
                        from scipy import signal
                        num_samples = int(len(audio_data) * 24000 / sample_rate)
                        audio_data = signal.resample(audio_data, num_samples).astype(np.int16)
                    
                    # Stream PCM data
                    chunk_size = 4096
                    for i in range(0, len(audio_data), chunk_size):
                        chunk = audio_data[i:i+chunk_size]
                        yield chunk.tobytes()
                        await asyncio.sleep(0.001)  # Small delay for streaming
                        
            finally:
                # Clean up temp file
                try:
                    Path(temp_path).unlink()
                except:
                    pass
            return
    
    # Fallback: Use macOS say command if TTS not available
    import subprocess
    import tempfile
    import wave
    import numpy as np
    
    with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as tmp_file:
        temp_path = tmp_file.name
    
    try:
        # Use macOS say to generate speech
        subprocess.run(['say', '-o', temp_path, text], check=True, capture_output=True)
        
        # Convert AIFF to WAV using ffmpeg
        wav_path = temp_path.replace('.aiff', '.wav')
        subprocess.run(['ffmpeg', '-i', temp_path, '-y', wav_path], 
                      check=True, capture_output=True)
        
        # Read WAV and convert to PCM
        with wave.open(wav_path, 'rb') as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            sample_rate = wav_file.getframerate()
            
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Resample to 24kHz
            if sample_rate != 24000:
                from scipy import signal
                num_samples = int(len(audio_data) * 24000 / sample_rate)
                audio_data = signal.resample(audio_data, num_samples).astype(np.int16)
            
            # Stream PCM data
            chunk_size = 4096
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i+chunk_size]
                yield chunk.tobytes()
                await asyncio.sleep(0.001)
                
    finally:
        # Clean up temp files
        for f in [temp_path, temp_path.replace('.aiff', '.wav')]:
            try:
                Path(f).unlink()
            except:
                pass


@app.post("/v1/audio/speech")
async def create_speech(request: SpeechRequest):
    """OpenAI-compatible speech endpoint"""
    try:
        return StreamingResponse(
            generate_speech_stream(request.input, request.voice),
            media_type="audio/pcm",
            headers={
                "Content-Type": "audio/pcm",
                "X-Audio-Sample-Rate": "24000",
                "X-Audio-Channels": "1",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "tts_available": TTS_AVAILABLE,
        "voices": list(VOICE_MODELS.keys())
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='OpenAI-compatible TTS API Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    
    args = parser.parse_args()
    
    print("🚀 Starting TTS API Server...")
    print(f"   URL: http://{args.host}:{args.port}")
    print(f"   TTS Available: {TTS_AVAILABLE}")
    if TTS_AVAILABLE:
        print(f"   Voices: {', '.join(VOICE_MODELS.keys())}")
    else:
        print("   ⚠️  Install TTS: pip install TTS")
    print("\n📡 Server ready! Use --open-source flag with voiceover script")
    print("-" * 60)
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()

