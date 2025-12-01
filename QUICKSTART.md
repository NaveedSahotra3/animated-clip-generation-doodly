# Quick Start Guide

Get up and running in 5 minutes!

## Installation (One-time setup)

```bash
# 1. Navigate to project directory
cd /Volumes/workspace/animated-clip-generation

# 2. Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# 3. Install everything
./scripts/install.sh

# 4. Download models (manual - see links below)
cd ~/Documents/ComfyUI
./download_models.sh
```

## Download Required Models

1. **DreamShaper XL** (6.5GB)
   - https://civitai.com/models/112902/dreamshaper-xl
   - Save to: `~/Documents/ComfyUI/models/checkpoints/`

2. **AnimateDiff Motion Module** (~700MB)
   - https://huggingface.co/guoyww/animatediff/tree/main
   - File: `mm_sd_v15_v2.ckpt`
   - Save to: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

## Generate Your First Clip

```bash
# 1. Start ComfyUI (in one terminal)
cd ~/Documents/ComfyUI
./launch_comfyui.sh

# 2. In ComfyUI browser (http://127.0.0.1:8188):
#    - Load workflow: workflows/whiteboard_animation.json
#    - Edit prompt: "simple line drawing of a man standing, white background, clean lines"
#    - Click "Queue Prompt"

# OR use Python script (in another terminal):
cd /Volumes/workspace/animated-clip-generation
python scripts/generate_clip.py \
  --prompt "simple line drawing of a man standing, white background, clean lines" \
  --duration 2
```

## Create a Complete Video

```bash
# 1. Create script file
cat > my_script.txt << EOF
Meet John. (2)
John walks home. (3)
John arrives. (2)
EOF

# 2. Generate all clips
python scripts/batch_generate.py --script my_script.txt

# 3. Generate voiceover
python scripts/generate_voiceover.py \
  --text "Meet John. John walks home. John arrives." \
  --output voiceover.wav

# 4. Assemble video
python scripts/assemble_video.py \
  --clips projects/output/clips \
  --voiceover voiceover.wav \
  --output final_video.mp4
```

## Next Steps

- Read `docs/WORKFLOW.md` for detailed workflow
- Check `docs/TROUBLESHOOTING.md` if you have issues
- See `templates/` for prompt examples

## Tips

- Start with short clips (2 seconds) for testing
- Use simple prompts first
- Check ComfyUI is running before generating
- Output files are in `projects/output/`

Happy creating! 🎨

