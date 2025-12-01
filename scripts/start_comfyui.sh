#!/bin/bash

# Start ComfyUI Server
# Usage: ./scripts/start_comfyui.sh

COMFYUI_DIR="$HOME/Documents/ComfyUI"

if [ ! -d "$COMFYUI_DIR" ]; then
    echo "Error: ComfyUI not found at $COMFYUI_DIR"
    echo "Please run ./scripts/install.sh first"
    exit 1
fi

cd "$COMFYUI_DIR"

if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run ./scripts/install.sh first"
    exit 1
fi

echo "Starting ComfyUI..."
echo "Access at: http://127.0.0.1:8188"
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
python main.py --force-fp16 --preview-method auto

