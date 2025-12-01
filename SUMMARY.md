# Codebase Summary

## Overview

Complete AI Whiteboard Video Generator codebase for M1 Max 32GB Mac. This system generates whiteboard-style animated videos locally using ComfyUI, AnimateDiff, and TTS.

## Project Structure

```
animated-clip-generation/
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── scripts/                     # Executable scripts
│   ├── install.sh              # Main installation script
│   ├── download_models.sh      # Model download helper
│   ├── start_comfyui.sh        # Start ComfyUI server
│   ├── generate_clip.py        # Single clip generation
│   ├── batch_generate.py       # Batch clip generation
│   ├── generate_voiceover.py   # TTS voiceover generation
│   └── assemble_video.py       # Video assembly
│
├── config/                      # Configuration files
│   ├── generation_config.yaml   # Generation settings
│   ├── prompts.yaml            # Prompt templates
│   ├── models.yaml             # Model configurations
│   └── generation_config.py    # Config loader
│
├── workflows/                   # ComfyUI workflow templates
│   ├── whiteboard_animation.json # AnimateDiff workflow
│   └── basic_image.json        # Basic image workflow
│
├── templates/                   # Prompt templates
│   ├── character_prompts.txt   # Character templates
│   ├── scene_prompts.txt       # Scene templates
│   └── action_prompts.txt      # Action templates
│
├── projects/                    # Project directories
│   └── example_project/
│       └── script.txt          # Example script
│
└── docs/                        # Documentation
    ├── SETUP.md                # Installation guide
    ├── WORKFLOW.md             # Usage workflow
    └── TROUBLESHOOTING.md      # Common issues
```

## Key Features

### 1. Automated Installation
- **install.sh**: Complete setup script
  - Installs Homebrew dependencies
  - Clones and sets up ComfyUI
  - Installs Python environment
  - Sets up custom nodes (AnimateDiff, Manager)
  - Creates directory structure

### 2. Clip Generation
- **generate_clip.py**: Single clip generation via ComfyUI API
  - Supports AnimateDiff workflows
  - Configurable duration, resolution, quality
  - Automatic download and saving
  
- **batch_generate.py**: Batch processing from script files
  - Parses script format: "Description (duration)"
  - Generates multiple clips in sequence
  - Creates manifest JSON for tracking

### 3. Voiceover Generation
- **generate_voiceover.py**: TTS integration
  - Supports Coqui TTS (high quality)
  - Supports Piper TTS (fast)
  - Supports macOS say (built-in)
  - Automatic format conversion

### 4. Video Assembly
- **assemble_video.py**: FFmpeg-based assembly
  - Combines clips into final video
  - Syncs voiceover audio
  - Supports manifest-based assembly
  - Configurable output settings

### 5. Configuration System
- **YAML configs**: Centralized settings
  - Generation parameters
  - Model paths and URLs
  - Prompt templates
  - Output directories

### 6. Workflow Templates
- **ComfyUI JSON workflows**: Pre-configured
  - Whiteboard animation workflow
  - Basic image workflow
  - Optimized for M1 Max

## Usage Flow

### 1. Installation
```bash
./scripts/install.sh
./scripts/download_models.sh  # Manual model download
```

### 2. Start ComfyUI
```bash
./scripts/start_comfyui.sh
```

### 3. Generate Clips
```bash
# Single clip
python scripts/generate_clip.py --prompt "..." --duration 2

# Batch from script
python scripts/batch_generate.py --script script.txt
```

### 4. Generate Voiceover
```bash
python scripts/generate_voiceover.py --text "..." --output voice.wav
```

### 5. Assemble Video
```bash
python scripts/assemble_video.py --clips clips/ --voiceover voice.wav --output final.mp4
```

## Technical Details

### Dependencies
- Python 3.10+
- PyTorch (M1 optimized)
- ComfyUI + AnimateDiff
- TTS libraries (Coqui/Piper)
- FFmpeg (for video assembly)

### Optimizations for M1 Max
- FP16 precision enabled
- Metal GPU acceleration
- Optimized resolution (768x768 default)
- Efficient memory usage
- Batch processing support

### File Formats
- Input: Script text files
- Intermediate: MP4 clips, WAV audio
- Output: MP4 video (H.264)

## Configuration

### Generation Settings
- Default resolution: 768x768
- Default steps: 25
- Default CFG scale: 7.5
- FPS: 24
- Frame count: 48 (2 seconds)

### Model Requirements
- Main checkpoint: DreamShaper XL (6.5GB) or ReV Animated (2GB)
- AnimateDiff: mm_sd_v15_v2.ckpt (~700MB)
- Optional: Sketch style LoRA

## Documentation

- **README.md**: Project overview
- **QUICKSTART.md**: 5-minute setup guide
- **docs/SETUP.md**: Detailed installation
- **docs/WORKFLOW.md**: Complete workflow guide
- **docs/TROUBLESHOOTING.md**: Common issues

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `install.sh` | Install all dependencies | `./scripts/install.sh` |
| `download_models.sh` | Show model download links | `./scripts/download_models.sh` |
| `start_comfyui.sh` | Start ComfyUI server | `./scripts/start_comfyui.sh` |
| `generate_clip.py` | Generate single clip | `python scripts/generate_clip.py --prompt "..."` |
| `batch_generate.py` | Generate multiple clips | `python scripts/batch_generate.py --script script.txt` |
| `generate_voiceover.py` | Generate TTS audio | `python scripts/generate_voiceover.py --text "..."` |
| `assemble_video.py` | Assemble final video | `python scripts/assemble_video.py --clips clips/ --output final.mp4` |

## Next Steps

1. Run `./scripts/install.sh` to set up
2. Download models (see `download_models.sh`)
3. Start ComfyUI and test generation
4. Create your first project
5. Read `docs/WORKFLOW.md` for detailed usage

## Support

- Check `docs/TROUBLESHOOTING.md` for common issues
- Review ComfyUI console for errors
- Verify all models are downloaded
- Test with simple prompts first

---

**Total Files Created**: 25+
**Lines of Code**: ~2000+
**Documentation Pages**: 5
**Ready to Use**: Yes ✅

