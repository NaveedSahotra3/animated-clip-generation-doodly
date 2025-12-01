# AI Whiteboard Video Generator

Complete local setup for generating whiteboard-style animated videos using ComfyUI, AnimateDiff, and TTS on M1 Max 32GB Mac.

## Quick Start

```bash
# 1. Run installation
cd /Volumes/workspace/animated-clip-generation
chmod +x scripts/*.sh scripts/*.py
./scripts/install.sh

# 2. Test installation
python scripts/test_installation.py

# 3. Download models (manual step)
cd ~/Documents/ComfyUI
./download_models.sh

# 4. Start ComfyUI
./launch_comfyui.sh

# 5. Generate a clip
python scripts/generate_clip.py --prompt "simple line drawing of a man standing" --duration 2
```

**📖 See `NEXT_STEPS.md` for detailed next steps after installation!**

## Project Structure

```
animated-clip-generation/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config/
│   ├── generation_config.yaml        # Generation settings
│   ├── prompts.yaml                  # Prompt templates
│   └── models.yaml                   # Model configurations
├── scripts/
│   ├── install.sh                    # Main installation script
│   ├── test_installation.py          # Verify installation
│   ├── download_models.sh            # Model download helper
│   ├── start_comfyui.sh              # Start ComfyUI server
│   ├── generate_clip.py              # Single clip generation
│   ├── batch_generate.py             # Batch clip generation
│   ├── generate_voiceover.py         # TTS voiceover generation
│   └── assemble_video.py             # Video assembly helper
├── workflows/
│   ├── basic_image.json              # Basic image generation workflow
│   ├── animatediff_simple.json       # Simple AnimateDiff workflow
│   └── whiteboard_animation.json      # Optimized whiteboard workflow
├── templates/
│   ├── character_prompts.txt          # Character prompt templates
│   ├── scene_prompts.txt              # Scene prompt templates
│   └── action_prompts.txt             # Action prompt templates
├── projects/                          # Your video projects
│   └── example_project/
│       ├── script.txt
│       ├── clips/
│       ├── voiceover/
│       └── final/
└── docs/
    ├── SETUP.md                      # Detailed setup guide
    ├── WORKFLOW.md                    # Workflow documentation
    └── TROUBLESHOOTING.md             # Common issues
```

## Features

- ✅ Automated ComfyUI installation
- ✅ AnimateDiff integration
- ✅ Batch clip generation
- ✅ Multiple TTS engines (Coqui, Piper, macOS)
- ✅ Prompt templates for whiteboard style
- ✅ Video assembly helpers
- ✅ Optimized for M1 Max 32GB

## Requirements

- macOS (M1 Max recommended)
- Homebrew
- Python 3.10+
- 50GB+ free disk space

## Documentation

See `docs/` directory for detailed guides:
- `SETUP.md` - Complete installation instructions
- `WORKFLOW.md` - How to create videos
- `TROUBLESHOOTING.md` - Common issues and solutions

**Quick Guides:**
- `QUICKSTART.md` - 5-minute quick start
- `INSTALLATION_STEPS.md` - Step-by-step installation
- `NEXT_STEPS.md` - What to do after installation
- `ALIGNMENT_CHECK.md` - Installation verification

## License

MIT

