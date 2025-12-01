#!/bin/bash

# ComfyUI Auto-Install Script for M1 Max
# This script automates the installation of ComfyUI and essential components
# Run this script: bash install_comfyui.sh

set -e  # Exit on error

echo "=================================="
echo "ComfyUI Installation for M1 Max"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Homebrew is installed
echo "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}Homebrew not found. Installing Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for M1 Macs
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo -e "${GREEN}✓ Homebrew already installed${NC}"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
brew install python@3.10 git wget

# Verify Python installation
echo ""
echo "Verifying Python 3.10..."
python3.10 --version

# Create installation directory
echo ""
echo "Setting up ComfyUI directory..."
cd ~/Documents
INSTALL_DIR="$HOME/Documents/ComfyUI"

# Clone ComfyUI
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}ComfyUI directory already exists. Skipping clone.${NC}"
    cd ComfyUI
else
    echo "Cloning ComfyUI..."
    git clone https://github.com/comfyanonymous/ComfyUI.git
    cd ComfyUI
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
else
    python3.10 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyTorch for M1 Mac
echo ""
echo "Installing PyTorch (M1 optimized)..."
pip install torch torchvision torchaudio

# Install ComfyUI requirements
echo ""
echo "Installing ComfyUI requirements..."
pip install -r requirements.txt

# Install additional useful packages
echo ""
echo "Installing additional packages..."
pip install opencv-python pillow

# Install ComfyUI Manager
echo ""
echo "Installing ComfyUI Manager..."
cd custom_nodes
if [ -d "ComfyUI-Manager" ]; then
    echo -e "${YELLOW}ComfyUI Manager already exists.${NC}"
else
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
fi

# Install AnimateDiff
echo ""
echo "Installing AnimateDiff..."
if [ -d "ComfyUI-AnimateDiff-Evolved" ]; then
    echo -e "${YELLOW}AnimateDiff already exists.${NC}"
else
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
fi

cd ..

# Create necessary directories
echo ""
echo "Creating model directories..."
mkdir -p models/checkpoints
mkdir -p models/loras
mkdir -p models/vae
mkdir -p models/controlnet
mkdir -p custom_nodes/ComfyUI-AnimateDiff-Evolved/models

# Create output directory
mkdir -p output

# Install Coqui TTS for voiceover
echo ""
echo "Installing Coqui TTS for voiceover generation..."
pip install TTS

# Create launch script
echo ""
echo "Creating launch script..."
cat > launch_comfyui.sh << 'EOF'
#!/bin/bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16 --preview-method auto
EOF

chmod +x launch_comfyui.sh

# Create helper script for model downloads
echo ""
echo "Creating model download helper script..."
cat > download_models.sh << 'EOF'
#!/bin/bash

echo "=================================="
echo "Model Download Helper"
echo "=================================="
echo ""
echo "Please download the following models manually:"
echo ""
echo "1. DreamShaper XL (Main Model - 6.5GB)"
echo "   URL: https://civitai.com/models/112902/dreamshaper-xl"
echo "   File: DreamShaperXL_v21TurboDPMSDE.safetensors"
echo "   Save to: ~/Documents/ComfyUI/models/checkpoints/"
echo ""
echo "2. AnimateDiff Motion Module"
echo "   URL: https://huggingface.co/guoyww/animatediff/tree/main"
echo "   File: mm_sd_v15_v2.ckpt"
echo "   Save to: ~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/"
echo ""
echo "3. (Optional) Sketch Style LoRA"
echo "   URL: https://civitai.com/search/models?query=sketch%20style"
echo "   Save to: ~/Documents/ComfyUI/models/loras/"
echo ""
echo "After downloading, run: ./launch_comfyui.sh"
EOF

chmod +x download_models.sh

# Create voiceover generation script
echo ""
echo "Creating voiceover helper script..."
cat > generate_voiceover.sh << 'EOF'
#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./generate_voiceover.sh \"Your text here\" output_name.wav"
    exit 1
fi

TEXT="$1"
OUTPUT="${2:-voiceover.wav}"

echo "Generating voiceover..."
source ~/Documents/ComfyUI/venv/bin/activate

tts --text "$TEXT" \
    --model_name tts_models/en/ljspeech/tacotron2-DDC \
    --out_path "$OUTPUT"

echo "Voiceover saved to: $OUTPUT"
EOF

chmod +x generate_voiceover.sh

# Create quick reference guide
cat > QUICK_START.md << 'EOF'
# ComfyUI Quick Start Guide

## Launch ComfyUI
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```
Then open: http://127.0.0.1:8188

## Download Required Models
```bash
./download_models.sh
```
Follow the instructions to download models manually.

## Generate Voiceover
```bash
./generate_voiceover.sh "Then John goes to home" john_voiceover.wav
```

## Project Structure
```
ComfyUI/
├── models/
│   ├── checkpoints/     # Put main models here
│   ├── loras/          # Put LoRA files here
│   └── vae/            # Put VAE files here
├── output/             # Generated videos/images
├── launch_comfyui.sh   # Start ComfyUI
└── generate_voiceover.sh # Generate voice

## Useful Commands

### Update ComfyUI
```bash
cd ~/Documents/ComfyUI
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Check GPU Usage
```bash
sudo powermetrics --samplers gpu_power -i 1000
```

### Clear Cache
Delete contents of: ~/Documents/ComfyUI/output/

## Troubleshooting

### ComfyUI won't start
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
pip install --upgrade torch torchvision torchaudio
```

### Models not showing
1. Check files are in correct folders
2. Refresh browser (F5)
3. Restart ComfyUI

### Slow generation
- Use --force-fp16 flag (already in launch script)
- Lower resolution to 512x512
- Reduce steps to 20

## Optimal Settings for M1 Max 32GB

**Image Generation:**
- Resolution: 768x768 or 1024x768
- Steps: 25-30
- CFG Scale: 7-8
- Sampler: DPM++ 2M Karras

**Video Generation (AnimateDiff):**
- Frames: 48 (2 sec) or 96 (4 sec)
- Resolution: 768x768
- Steps: 20-25
- Context: 16

## Prompt Templates

### Character (Static)
```
Positive: "simple line drawing of [character], white background, clean black lines, minimalist sketch, hand drawn style, full body"

Negative: "colored, realistic, complex background, shadows, multiple characters"
```

### Animation
```
Positive: "animated sketch of [action], white background, smooth motion, clean lines, hand drawn animation"

Negative: "static, colored, complex, realistic"
```

## Next Steps

1. Download models using ./download_models.sh
2. Launch ComfyUI with ./launch_comfyui.sh
3. Try generating a test image
4. Generate your first 2-second animation
5. Edit in Premiere Pro/After Effects

## Resources

- ComfyUI Wiki: https://github.com/comfyanonymous/ComfyUI/wiki
- Models: https://civitai.com
- Workflows: https://comfyworkflows.com
EOF

echo ""
echo -e "${GREEN}=================================="
echo "Installation Complete!"
echo -e "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Download models: ./download_models.sh"
echo "2. Launch ComfyUI: ./launch_comfyui.sh"
echo "3. Open browser: http://127.0.0.1:8188"
echo ""
echo "Quick reference: Read QUICK_START.md"
echo ""
echo -e "${YELLOW}Important: You must download models before first use!${NC}"
echo "Run: ./download_models.sh for download links"
echo ""