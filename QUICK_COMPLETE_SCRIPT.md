# 🚀 Quick Complete Script Guide

## Commands to Run (In Order)

### 1. Start ComfyUI (Image Generation)
```bash
./scripts/start_comfyui.sh
```
Wait for: "Starting server" message

### 2. Start TTS Server (Voice Generation)
```bash
./scripts/start_tts_server.sh
```
Wait for: "Server ready!" message

### 3. Generate All Scenes
```bash
python3 scripts/generate_complete_scenes.py
```

**Output:** `output/survival/script/`
- Images: `scene_1.png` through `scene_10.png`
- Voices: `voice_scene_1_A.mp3`, `voice_scene_2_A.mp3`, etc.

---

## Stop Servers
```bash
pkill -f tts_api_server.py
pkill -f comfyui
```

---

## File Structure
```
output/survival/script/
├── scene_1.png
├── voice_scene_1_A.mp3
├── scene_2.png
├── voice_scene_2_A.mp3
└── ...
```

---

## Script File
Edit scenes in: `scripts/complete_script.json`

