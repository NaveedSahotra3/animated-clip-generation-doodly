#!/bin/bash

# Verify Model Downloads
# Checks if required models are in the correct locations

COMFYUI_DIR="$HOME/Documents/ComfyUI"
CHECKPOINTS_DIR="$COMFYUI_DIR/models/checkpoints"
ANIMATEDIFF_DIR="$COMFYUI_DIR/custom_nodes/ComfyUI-AnimateDiff-Evolved/models"

echo "=================================="
echo "Model Verification"
echo "=================================="
echo ""

# Check AnimateDiff
echo "AnimateDiff Motion Module:"
if [ -f "$ANIMATEDIFF_DIR/mm_sd_v15_v2.ckpt" ]; then
    size=$(du -h "$ANIMATEDIFF_DIR/mm_sd_v15_v2.ckpt" | cut -f1)
    echo "  ✅ Found: mm_sd_v15_v2.ckpt ($size)"
else
    echo "  ❌ Missing: mm_sd_v15_v2.ckpt"
fi

echo ""
echo "DreamShaper XL Checkpoint:"
if [ -f "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" ]; then
    size=$(du -h "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" | cut -f1)
    echo "  ✅ Found: DreamShaperXL_v21TurboDPMSDE.safetensors ($size)"
elif ls "$CHECKPOINTS_DIR"/*dreamshaper*.safetensors 1> /dev/null 2>&1 || ls "$CHECKPOINTS_DIR"/*DreamShaper*.safetensors 1> /dev/null 2>&1; then
    echo "  ✅ Found DreamShaper XL model:"
    ls -lh "$CHECKPOINTS_DIR"/*[Dd]ream[Ss]haper*.safetensors 2>/dev/null | awk '{print "    " $9 " (" $5 ")"}'
else
    echo "  ❌ Missing: DreamShaper XL model"
    echo ""
    echo "  Files in checkpoints directory:"
    ls -lh "$CHECKPOINTS_DIR" 2>/dev/null || echo "    (directory empty or doesn't exist)"
fi

echo ""
echo "=================================="
if [ -f "$ANIMATEDIFF_DIR/mm_sd_v15_v2.ckpt" ] && ( ls "$CHECKPOINTS_DIR"/*[Dd]ream[Ss]haper*.safetensors 1> /dev/null 2>&1 || [ -f "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" ] ); then
    echo "✅ All models ready!"
    echo ""
    echo "You can now start ComfyUI:"
    echo "  cd ~/Documents/ComfyUI"
    echo "  ./launch_comfyui.sh"
else
    echo "⚠️  Some models are missing"
    echo ""
    echo "Please download missing models and run this script again to verify."
fi

