# Setup Guide

Complete installation guide for AI Whiteboard Video Generator on M1 Max 32GB Mac.

## Prerequisites

- macOS (M1 Max recommended)
- 50GB+ free disk space
- Internet connection for downloads

## Quick Installation

```bash
# 1. Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# 2. Run installation
./scripts/install.sh

# 3. Download models (manual step)
./scripts/download_models.sh

# 4. Start ComfyUI
./scripts/start_comfyui.sh
```

## Detailed Steps

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Run Installation Script

The installation script will:
- Install system dependencies (Python 3.10, git, wget)
- Clone ComfyUI to `~/Documents/ComfyUI`
- Set up Python virtual environment
- Install PyTorch (M1 optimized)
- Install ComfyUI and custom nodes
- Install TTS libraries

```bash
./scripts/install.sh
```

### Step 3: Download Models

Models must be downloaded manually due to size and licensing:

1. **Main Checkpoint** (choose one):
   - DreamShaper XL (6.5GB) - Recommended
   - ReV Animated (2GB) - Alternative
   
2. **AnimateDiff Motion Module**:
   - `mm_sd_v15_v2.ckpt` for SD 1.5 models
   - `mm_sdxl_v10_beta.ckpt` for SDXL models

3. **Optional LoRA**:
   - Sketch style LoRA for enhanced line art

See `./scripts/download_models.sh` for download links.

### Step 4: Verify Installation

```bash
# Start ComfyUI
./scripts/start_comfyui.sh

# Open browser: http://127.0.0.1:8188
# You should see the ComfyUI interface
```

## Troubleshooting

### ComfyUI won't start

```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
pip install --upgrade torch torchvision torchaudio
python main.py --force-fp16
```

### Models not showing

1. Check files are in correct folders:
   - Checkpoints: `~/Documents/ComfyUI/models/checkpoints/`
   - AnimateDiff: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`
2. Refresh browser (F5)
3. Restart ComfyUI

### Out of memory errors

- Reduce resolution to 512x512
- Lower batch size to 1
- Close other applications

## Next Steps

After installation:
1. Read `docs/WORKFLOW.md` for usage guide
2. Try generating a test clip
3. Create your first project

