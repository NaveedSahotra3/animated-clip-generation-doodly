# Workflow Guide

Complete guide to creating whiteboard animation videos.

## Overview

The workflow consists of 4 main steps:
1. **Generate Clips** - Create animated segments
2. **Generate Voiceover** - Create narration audio
3. **Assemble Video** - Combine clips and audio
4. **Post-Process** - Edit in Premiere/After Effects (optional)

## Step 1: Generate Clips

### Single Clip

```bash
python scripts/generate_clip.py \
  --prompt "simple line drawing of a man standing, white background, clean lines" \
  --duration 2 \
  --output output/clips
```

### Batch Generation from Script

1. Create a script file (see `projects/example_project/script.txt`):

```
Meet John. (2)
John walks to his home. (3)
John arrives at home. (4)
```

2. Generate all clips:

```bash
python scripts/batch_generate.py \
  --script projects/example_project/script.txt \
  --output projects/example_project/clips
```

### Prompt Tips

- Use "simple line drawing" for whiteboard style
- Include "white background, clean black lines"
- Add "minimalist sketch, hand drawn style"
- Negative prompt: "colored, realistic, complex background"

See `templates/` for more prompt examples.

## Step 2: Generate Voiceover

### Using macOS say (easiest)

```bash
python scripts/generate_voiceover.py \
  --text "Then John goes to home" \
  --engine macos \
  --output voiceover.wav
```

### Using Coqui TTS (better quality)

```bash
python scripts/generate_voiceover.py \
  --text "Then John goes to home" \
  --engine coqui \
  --output voiceover.wav
```

## Step 3: Assemble Video

### From clips directory

```bash
python scripts/assemble_video.py \
  --clips projects/example_project/clips \
  --voiceover projects/example_project/voiceover/narration.wav \
  --output projects/example_project/final/video.mp4
```

### From manifest

```bash
python scripts/assemble_video.py \
  --manifest projects/example_project/clips/manifest.json \
  --voiceover projects/example_project/voiceover/narration.wav \
  --output projects/example_project/final/video.mp4
```

## Step 4: Post-Processing (Optional)

### After Effects

1. Import clips and voiceover
2. Create composition (1920x1080, 24fps)
3. Add drawing effects:
   - Effect → Generate → Scribble
   - Effect → Generate → Stroke
4. Add hand overlay (download from Pixabay)
5. Sync voiceover
6. Export: H.264, 1920x1080

### Premiere Pro

1. Create sequence (1920x1080, 24fps)
2. Import clips to timeline
3. Add transitions
4. Add voiceover track
5. Add hand overlay videos
6. Color correction (pure white background)
7. Export: H.264, high quality

## Complete Example

```bash
# 1. Generate clips
python scripts/batch_generate.py \
  --script projects/example_project/script.txt \
  --output projects/example_project/clips

# 2. Generate voiceover
python scripts/generate_voiceover.py \
  --text "Meet John. John is a friendly guy who loves his home." \
  --output projects/example_project/voiceover/narration.wav

# 3. Assemble video
python scripts/assemble_video.py \
  --clips projects/example_project/clips \
  --voiceover projects/example_project/voiceover/narration.wav \
  --output projects/example_project/final/video.mp4
```

## Tips

- **Consistency**: Use same seed for related clips
- **Timing**: Match clip duration to script timing
- **Quality**: Use balanced preset (25 steps, 768x768) for best speed/quality
- **Testing**: Generate short test clips before batch processing

## Troubleshooting

### Clips don't match style
- Use consistent prompts
- Use same seed value
- Consider using LoRA for style consistency

### Video assembly fails
- Check all clips exist
- Verify ffmpeg is installed: `brew install ffmpeg`
- Check file formats (MP4 recommended)

### Voiceover out of sync
- Adjust timing in editing software
- Regenerate with different pacing
- Use script timing as guide

