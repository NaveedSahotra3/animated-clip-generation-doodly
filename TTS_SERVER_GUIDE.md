# TTS API Server Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn scipy
pip install TTS  # For text-to-speech
```

### 2. Start the Server

```bash
# Option 1: Use the script
./scripts/start_tts_server.sh

# Option 2: Direct Python
python3 scripts/tts_api_server.py
```

Server runs on: **http://localhost:8000**

### 3. Generate Voiceover

```bash
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --open-source
```

---

## 📋 Server Options

```bash
# Custom port
python3 scripts/tts_api_server.py --port 3000

# Custom host
python3 scripts/tts_api_server.py --host 0.0.0.0

# Auto-reload (for development)
python3 scripts/tts_api_server.py --reload
```

---

## ✅ Features

- **OpenAI-compatible API** - Works with existing scripts
- **No API key required** - Runs locally
- **Onyx voice support** - Deep, dramatic male voice
- **Streaming responses** - Efficient for long texts
- **Multiple voices** - onyx, alloy, echo, fable, nova, shimmer, coral

---

## 🔧 Troubleshooting

**"TTS library not available"**
```bash
pip install TTS
```

**"fastapi not found"**
```bash
pip install fastapi uvicorn
```

**Port already in use**
```bash
python3 scripts/tts_api_server.py --port 8001
# Then use --base-url "http://localhost:8001/v1"
```

---

## 📡 API Endpoints

- `POST /v1/audio/speech` - Generate speech (OpenAI-compatible)
- `GET /health` - Health check

---

## 🎤 Voice Options

All voices use the same TTS model but can be customized:
- `onyx` - Deep, dramatic (default)
- `alloy`, `echo`, `fable`, `nova`, `shimmer`, `coral`

---

## 💡 Usage Workflow

1. **Terminal 1:** Start TTS server
   ```bash
   ./scripts/start_tts_server.sh
   ```

2. **Terminal 2:** Generate voiceover
   ```bash
   python3 scripts/generate_openai_voiceover.py \
     --file templates/youtube_ai_voice_generation.txt \
     --open-source
   ```

---

## 🔄 Background Mode

Run server in background:
```bash
nohup python3 scripts/tts_api_server.py > tts_server.log 2>&1 &
```

Stop it:
```bash
pkill -f tts_api_server.py
```

