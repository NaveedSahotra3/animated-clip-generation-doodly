#!/bin/bash

# AI Whiteboard Video Generator - Installation Script
# For M1 Max 32GB Mac

set -e

echo "=================================="
echo "AI Whiteboard Video Generator"
echo "Installation Script"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMFYUI_DIR="$HOME/Documents/ComfyUI"

# Step 1: Check Homebrew
echo -e "${BLUE}[1/8]${NC} Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}Homebrew not found. Installing...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add to PATH for M1 Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo -e "${GREEN}✓ Homebrew installed${NC}"
fi

# Step 2: Install system dependencies
echo ""
echo -e "${BLUE}[2/8]${NC} Installing system dependencies..."
brew install python@3.10 git wget || true

# Verify Python
if ! command -v python3.10 &> /dev/null; then
    echo -e "${RED}Error: Python 3.10 not found. Please install manually.${NC}"
    exit 1
fi

# Step 3: Install ComfyUI
echo ""
echo -e "${BLUE}[3/8]${NC} Setting up ComfyUI..."
if [ -d "$COMFYUI_DIR" ]; then
    echo -e "${YELLOW}ComfyUI already exists at $COMFYUI_DIR${NC}"
    echo -e "${YELLOW}Skipping clone. Use 'git pull' to update.${NC}"
else
    echo "Cloning ComfyUI to $COMFYUI_DIR..."
    mkdir -p "$HOME/Documents"
    cd "$HOME/Documents"
    git clone https://github.com/comfyanonymous/ComfyUI.git
fi

cd "$COMFYUI_DIR"

# Step 4: Create virtual environment
echo ""
echo -e "${BLUE}[4/8]${NC} Setting up Python environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
else
    python3.10 -m venv venv
fi

source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Step 5: Install PyTorch and dependencies
echo ""
echo -e "${BLUE}[5/8]${NC} Installing PyTorch (M1 optimized)..."
pip install torch torchvision torchaudio

# Step 6: Install ComfyUI requirements
echo ""
echo -e "${BLUE}[6/8]${NC} Installing ComfyUI requirements..."
pip install -r requirements.txt

# Install project dependencies
echo ""
echo "Installing project dependencies..."
pip install -r "$PROJECT_DIR/requirements.txt"

# Step 7: Install custom nodes
echo ""
echo -e "${BLUE}[7/8]${NC} Installing custom nodes..."
cd custom_nodes

# ComfyUI Manager
if [ ! -d "ComfyUI-Manager" ]; then
    echo "Installing ComfyUI Manager..."
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
fi

# AnimateDiff
if [ ! -d "ComfyUI-AnimateDiff-Evolved" ]; then
    echo "Installing AnimateDiff..."
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
fi

cd "$COMFYUI_DIR"

# Step 8: Create directories
echo ""
echo -e "${BLUE}[8/8]${NC} Creating directory structure..."
mkdir -p models/checkpoints
mkdir -p models/loras
mkdir -p models/vae
mkdir -p models/controlnet
mkdir -p custom_nodes/ComfyUI-AnimateDiff-Evolved/models
mkdir -p output

# Create launch script
echo ""
echo "Creating helper scripts in ComfyUI directory..."
cat > "$COMFYUI_DIR/launch_comfyui.sh" << 'EOF'
#!/bin/bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16 --preview-method auto
EOF
chmod +x "$COMFYUI_DIR/launch_comfyui.sh"

# Create download models helper
cat > "$COMFYUI_DIR/download_models.sh" << 'EOF'
#!/bin/bash
echo "=================================="
echo "Required Model Downloads"
echo "=================================="
echo ""
echo "📥 1. DreamShaper XL (Main Model - 6.5GB)"
echo "   URL: https://civitai.com/models/112902/dreamshaper-xl"
echo "   Download: DreamShaperXL_v21TurboDPMSDE.safetensors"
echo "   Save to: ~/Documents/ComfyUI/models/checkpoints/"
echo ""
echo "📥 2. AnimateDiff Motion Module"
echo "   URL: https://huggingface.co/guoyww/animatediff/tree/main"
echo "   Download: mm_sd_v15_v2.ckpt"
echo "   Save to: ~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/"
echo ""
echo "After downloading, run: ./launch_comfyui.sh"
EOF
chmod +x "$COMFYUI_DIR/download_models.sh"

# Create voiceover helper script
cat > "$COMFYUI_DIR/generate_voiceover.sh" << 'EOF'
#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./generate_voiceover.sh \"Your text\" output.wav"
    exit 1
fi
cd ~/Documents/ComfyUI
source venv/bin/activate
tts --text "$1" --model_name tts_models/en/ljspeech/tacotron2-DDC --out_path "${2:-voiceover.wav}"
echo "Saved to: ${2:-voiceover.wav}"
EOF
chmod +x "$COMFYUI_DIR/generate_voiceover.sh"

echo ""
echo -e "${GREEN}=================================="
echo "Installation Complete!"
echo -e "==================================${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. cd ~/Documents/ComfyUI"
echo "2. ./download_models.sh  (see download links)"
echo "3. Download the 2 required models manually"
echo "4. ./launch_comfyui.sh  (start ComfyUI)"
echo "5. Open browser: http://127.0.0.1:8188"
echo ""
echo -e "${YELLOW}Important: Download models before first use!${NC}"
echo ""
echo "Helper scripts created in ComfyUI directory:"
echo "  - launch_comfyui.sh (start ComfyUI)"
echo "  - download_models.sh (show download links)"
echo "  - generate_voiceover.sh (generate TTS)"
echo ""
echo "Project scripts also available in: $PROJECT_DIR/scripts/"
echo ""

