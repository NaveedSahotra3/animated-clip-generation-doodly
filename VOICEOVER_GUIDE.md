# Voiceover Generation Guide

## 🎤 OpenAI TTS with Onyx Voice (Dramatic)

This script generates high-quality voiceover using OpenAI's TTS API with the **Onyx** voice and **dramatic** vibe.

### Features

✅ **Automatic Text Chunking** - Handles long texts by splitting into manageable chunks  
✅ **Onyx Voice** - Deep, dramatic male voice with excellent bass  
✅ **MP3 Output** - Converts from PCM/WAV to MP3 format  
✅ **Smart Merging** - Seamlessly combines multiple chunks  
✅ **Dramatic Instructions** - Pre-configured for intense, powerful delivery  

---

## 🚀 Quick Start

### 1. Set Up API Key

```bash
# Option 1: Environment variable (recommended)
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Pass via command line (see below)
```

### 2. Generate Voiceover

```bash
# Basic usage
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt

# With custom output location
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --output output/survival/voiceover.mp3
```

---

## 📋 Command Options

```bash
python3 scripts/generate_openai_voiceover.py \
  --file <text_file>              # Required: Text file to convert
  --output <output_path>           # Output MP3 file (default: output/survival/voiceover.mp3)
  --api-key <key>                  # OpenAI API key (or use OPENAI_API_KEY env var)
  --chunk-size <number>            # Max characters per chunk (default: 1000)
  --voice <voice_name>             # Voice: onyx, alloy, echo, fable, nova, shimmer (default: onyx)
  --open-source                     # Use open source API alternative
  --instructions <text>            # Custom voice instructions (optional)
```

---

## 🎯 Voice Options

| Voice | Description | Best For |
|-------|-------------|----------|
| **onyx** | Deep, dramatic male voice with bass | **Dramatic narrations (RECOMMENDED)** |
| alloy | Balanced, neutral voice | General purpose |
| echo | Clear, professional voice | Educational content |
| fable | Warm, storytelling voice | Stories |
| nova | Energetic, expressive voice | Dynamic content |
| shimmer | Soft, gentle voice | Calm content |

**Default:** `onyx` (dramatic, male, deep bass)

---

## ⚙️ Chunk Size

The script automatically splits long text into chunks to respect API limits:

- **Default:** 1000 characters per chunk
- **Custom:** Use `--chunk-size` to adjust
- **Smart Splitting:** Breaks at sentence boundaries when possible

**Example:**
```bash
# Smaller chunks (if API has stricter limits)
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --chunk-size 800

# Larger chunks (if API allows)
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --chunk-size 2000
```

---

## 🔧 Open Source API Alternative

If you have an open source API running (like the example you provided), use:

```bash
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --open-source
```

**Note:** You may need to modify the script to set the correct `base_url` for your open source API.

---

## 📁 Output Structure

```
output/
  └── survival/
      ├── voiceover.mp3          # Final merged voiceover
      └── images/                 # Your scene images
          ├── scene-1.png
          ├── scene-2.png
          └── ...
```

---

## 🎨 Dramatic Voice Instructions

The script uses pre-configured dramatic instructions for the Onyx voice:

```
Voice Affect: Dramatic, powerful, and commanding; project authority and intensity.

Tone: Serious, intense, and compelling—express urgency and importance.

Pacing: Varied and dynamic; slower for emphasis on key points, faster for building tension.

Emotion: Strong conviction and gravitas; speak with deep resonance and bass.

Pronunciation: Clear and precise, emphasizing critical words to reinforce impact.

Pauses: Strategic pauses after important statements, creating dramatic effect.
```

**Custom Instructions:**
```bash
python3 scripts/generate_openai_voiceover.py \
  --file templates/youtube_ai_voice_generation.txt \
  --instructions "Your custom instructions here"
```

---

## 🔄 Workflow

1. **Prepare Text File**
   - Edit `templates/youtube_ai_voice_generation.txt`
   - Add your script/narration

2. **Generate Voiceover**
   ```bash
   python3 scripts/generate_openai_voiceover.py \
     --file templates/youtube_ai_voice_generation.txt
   ```

3. **Output**
   - MP3 file saved to `output/survival/voiceover.mp3`
   - Ready to use in Premiere Pro/After Effects

4. **Combine with Images**
   - Use `scripts/assemble_video.py` to combine voiceover with scene images
   - Or import manually into your video editor

---

## 💡 Tips

1. **API Key Security**
   - Use environment variables instead of command-line flags
   - Never commit API keys to git

2. **Chunk Size**
   - Start with default (1000 chars)
   - Reduce if you hit API limits
   - Increase if API allows longer text

3. **Voice Selection**
   - Onyx is best for dramatic, serious content
   - Try other voices if you want different tones

4. **Text Formatting**
   - Use proper punctuation for natural pauses
   - Break long sentences for better pacing
   - Add line breaks for paragraph pauses

---

## 🆘 Troubleshooting

### "OpenAI API key not found"
```bash
export OPENAI_API_KEY="your-key-here"
```

### "ffmpeg not found"
```bash
brew install ffmpeg
```

### "openai library not installed"
```bash
pip install openai
```

### Chunks not merging properly
- Check that all chunks were generated successfully
- Verify ffmpeg is installed and working
- Check temp directory for individual chunk files

---

## 📊 Expected Output

- **Format:** MP3
- **Bitrate:** 192kbps
- **Sample Rate:** 24kHz (from OpenAI TTS)
- **Channels:** Mono
- **Duration:** ~150 words per minute (estimated)

---

## 🎬 Next Steps

After generating voiceover:

1. **Review the MP3** - Check quality and pacing
2. **Import to Video Editor** - Premiere Pro, After Effects, etc.
3. **Sync with Images** - Match voiceover to scene images
4. **Final Export** - Create your YouTube video!

---

## 📖 Related Files

- `templates/youtube_ai_voice_generation.txt` - Your script text
- `scripts/generate_openai_voiceover.py` - Voiceover generation script
- `output/survival/voiceover.mp3` - Generated voiceover
- `scripts/assemble_video.py` - Combine voiceover with images

