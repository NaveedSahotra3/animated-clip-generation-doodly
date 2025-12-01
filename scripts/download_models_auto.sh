#!/bin/bash

# Automated Model Download Script
# Attempts to download models directly if possible

set -e

COMFYUI_DIR="$HOME/Documents/ComfyUI"
CHECKPOINTS_DIR="$COMFYUI_DIR/models/checkpoints"
ANIMATEDIFF_DIR="$COMFYUI_DIR/custom_nodes/ComfyUI-AnimateDiff-Evolved/models"

echo "=================================="
echo "Automated Model Download"
echo "=================================="
echo ""

# Create directories
mkdir -p "$CHECKPOINTS_DIR"
mkdir -p "$ANIMATEDIFF_DIR"

# Function to download with progress
download_file() {
    local url=$1
    local output=$2
    local name=$3
    
    echo "Downloading $name..."
    echo "URL: $url"
    echo "Output: $output"
    echo ""
    
    if command -v wget &> /dev/null; then
        wget --progress=bar:force -O "$output" "$url" || {
            echo "⚠ wget failed, trying curl..."
            curl -L --progress-bar -o "$output" "$url" || {
                echo "❌ Download failed for $name"
                echo "Please download manually from: $url"
                return 1
            }
        }
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar -o "$output" "$url" || {
            echo "❌ Download failed for $name"
            echo "Please download manually from: $url"
            return 1
        }
    else
        echo "❌ Neither wget nor curl found. Please install one."
        return 1
    fi
    
    if [ -f "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        echo "✅ Downloaded: $name ($size)"
        return 0
    else
        echo "❌ File not found after download"
        return 1
    fi
}

# Try to download AnimateDiff motion module from HuggingFace
echo "📥 Attempting to download AnimateDiff Motion Module..."
echo ""

# HuggingFace direct download URL (may require authentication for some models)
ANIMATEDIFF_URL="https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
ANIMATEDIFF_OUTPUT="$ANIMATEDIFF_DIR/mm_sd_v15_v2.ckpt"

if [ -f "$ANIMATEDIFF_OUTPUT" ]; then
    echo "✅ AnimateDiff motion module already exists"
else
    echo "Attempting direct download from HuggingFace..."
    download_file "$ANIMATEDIFF_URL" "$ANIMATEDIFF_OUTPUT" "AnimateDiff Motion Module" || {
        echo ""
        echo "⚠ Direct download failed. HuggingFace may require authentication."
        echo "Please download manually:"
        echo "  1. Go to: https://huggingface.co/guoyww/animatediff/tree/main"
        echo "  2. Click on 'mm_sd_v15_v2.ckpt'"
        echo "  3. Click download button"
        echo "  4. Save to: $ANIMATEDIFF_DIR"
        echo ""
    }
fi

# DreamShaper XL - Civitai requires manual download
echo ""
echo "📥 DreamShaper XL Model..."
echo ""
echo "⚠ Civitai models require manual download (browser required)"
echo ""
echo "Please download manually:"
echo "  1. Go to: https://civitai.com/models/112902/dreamshaper-xl"
echo "  2. Click 'Download' button"
echo "  3. Select: DreamShaperXL_v21TurboDPMSDE.safetensors"
echo "  4. Save to: $CHECKPOINTS_DIR"
echo ""
echo "Or try alternative download method:"
echo "  - Use Civitai API if you have an API key"
echo "  - Use browser extension for direct downloads"
echo ""

# Check if DreamShaper already exists
if [ -f "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" ]; then
    echo "✅ DreamShaper XL model already exists"
elif ls "$CHECKPOINTS_DIR"/*DreamShaper*.safetensors 1> /dev/null 2>&1; then
    echo "✅ Found DreamShaper model (different version)"
    ls -lh "$CHECKPOINTS_DIR"/*DreamShaper*.safetensors
else
    echo "❌ DreamShaper XL not found"
fi

echo ""
echo "=================================="
echo "Download Summary"
echo "=================================="
echo ""

# Check what we have
echo "AnimateDiff Motion Module:"
if [ -f "$ANIMATEDIFF_OUTPUT" ]; then
    size=$(du -h "$ANIMATEDIFF_OUTPUT" | cut -f1)
    echo "  ✅ Found: $ANIMATEDIFF_OUTPUT ($size)"
else
    echo "  ❌ Missing: $ANIMATEDIFF_OUTPUT"
fi

echo ""
echo "DreamShaper XL Checkpoint:"
if [ -f "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" ]; then
    size=$(du -h "$CHECKPOINTS_DIR/DreamShaperXL_v21TurboDPMSDE.safetensors" | cut -f1)
    echo "  ✅ Found: DreamShaperXL_v21TurboDPMSDE.safetensors ($size)"
elif ls "$CHECKPOINTS_DIR"/*DreamShaper*.safetensors 1> /dev/null 2>&1; then
    echo "  ✅ Found alternative DreamShaper version"
    ls -lh "$CHECKPOINTS_DIR"/*DreamShaper*.safetensors | awk '{print "    " $9 " (" $5 ")"}'
else
    echo "  ❌ Missing: DreamShaperXL_v21TurboDPMSDE.safetensors"
    echo "     Download from: https://civitai.com/models/112902/dreamshaper-xl"
fi

echo ""
echo "=================================="
echo "Next Steps"
echo "=================================="
echo ""
echo "If models are downloaded:"
echo "  1. cd ~/Documents/ComfyUI"
echo "  2. ./launch_comfyui.sh"
echo "  3. Open: http://127.0.0.1:8188"
echo ""
echo "If models are missing, download manually using the links above."

