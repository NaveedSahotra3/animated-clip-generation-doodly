# 🎤 Quick Voiceover Generation

## Fastest Way to Generate Voiceover

```bash
# 1. Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 2. Generate voiceover
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt
```

**Output:** `output/survival/voiceover.mp3`

---

## What It Does

✅ Reads your text from `templates/youtube_ai_voice_generation.txt`  
✅ Splits into chunks (1000 chars each) to handle API limits  
✅ Uses **Onyx voice** with **dramatic vibe** (deep, male, bass)  
✅ Converts to **MP3 format**  
✅ Merges all chunks seamlessly  

---

## Custom Options

```bash
# Smaller chunks (if API has stricter limits)
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --chunk-size 800

# Custom output location
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --output output/my_voiceover.mp3

# Different voice (if you want to try others)
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --voice nova
```

---

## Prerequisites

1. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Set: `export OPENAI_API_KEY="your-key"`

2. **FFmpeg** (for MP3 conversion)
   ```bash
   brew install ffmpeg
   ```

3. **OpenAI Library**
   ```bash
   pip install openai
   ```

---

## File Locations

- **Input:** `templates/youtube_ai_voice_generation.txt`
- **Output:** `output/survival/voiceover.mp3`

---

## Troubleshooting

**"API key not found"**
```bash
export OPENAI_API_KEY="your-key-here"
```

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**"openai library not installed"**
```bash
pip install openai
```

---

See `VOICEOVER_GUIDE.md` for complete documentation.

