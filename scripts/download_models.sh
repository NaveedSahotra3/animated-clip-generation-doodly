#!/bin/bash

# Model Download Helper Script
# Provides instructions and direct download links for required models

echo "=================================="
echo "Model Download Guide"
echo "=================================="
echo ""

COMFYUI_DIR="$HOME/Documents/ComfyUI"

# Check if ComfyUI is installed
if [ ! -d "$COMFYUI_DIR" ]; then
    echo "Error: ComfyUI not found at $COMFYUI_DIR"
    echo "Please run ./scripts/install.sh first"
    exit 1
fi

echo "Required Models:"
echo ""
echo "1. MAIN CHECKPOINT (Choose one):"
echo "   Option A: DreamShaper XL (Recommended - 6.5GB)"
echo "   URL: https://civitai.com/models/112902/dreamshaper-xl"
echo "   File: DreamShaperXL_v21TurboDPMSDE.safetensors"
echo "   Save to: $COMFYUI_DIR/models/checkpoints/"
echo ""
echo "   Option B: ReV Animated (Alternative - 2GB)"
echo "   URL: https://civitai.com/models/7371/rev-animated"
echo "   File: revAnimated_v122.safetensors"
echo "   Save to: $COMFYUI_DIR/models/checkpoints/"
echo ""
echo "2. ANIMATEDIFF MOTION MODULE:"
echo "   URL: https://huggingface.co/guoyww/animatediff/tree/main"
echo "   File: mm_sd_v15_v2.ckpt (for SD 1.5) or mm_sdxl_v10_beta.ckpt (for SDXL)"
echo "   Save to: $COMFYUI_DIR/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/"
echo ""
echo "3. (Optional) SKETCH STYLE LoRA:"
echo "   Search: https://civitai.com/search/models?query=sketch%20style"
echo "   Recommended: 'Sketch Style LoRA' or 'Hand Drawn Style'"
echo "   Save to: $COMFYUI_DIR/models/loras/"
echo ""
echo "Creating directories..."
mkdir -p "$COMFYUI_DIR/models/checkpoints"
mkdir -p "$COMFYUI_DIR/models/loras"
mkdir -p "$COMFYUI_DIR/custom_nodes/ComfyUI-AnimateDiff-Evolved/models"
echo ""
echo "Directories created. Please download models manually using the links above."
echo ""
echo "After downloading, restart ComfyUI to load the models."

