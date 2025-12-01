# Model Download Status

## ✅ Successfully Downloaded

### AnimateDiff Motion Module
- **File**: `mm_sd_v15_v2.ckpt`
- **Size**: 1.7 GB
- **Location**: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`
- **Status**: ✅ Complete

## ⚠️ Manual Download Required

### DreamShaper XL
- **File**: `DreamShaperXL_v21TurboDPMSDE.safetensors`
- **Size**: ~6.5 GB
- **Location**: `~/Documents/ComfyUI/models/checkpoints/`
- **Status**: ❌ Not downloaded (requires browser)

### How to Download DreamShaper XL

**Option 1: Browser Download (Recommended)**
1. Open browser: https://civitai.com/models/112902/dreamshaper-xl
2. Click the "Download" button
3. Select version: `DreamShaperXL_v21TurboDPMSDE.safetensors`
4. Save to: `~/Documents/ComfyUI/models/checkpoints/`

**Option 2: Using Civitai API (if you have API key)**
```bash
# Requires Civitai API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://civitai.com/api/download/models/112902" \
  -o ~/Documents/ComfyUI/models/checkpoints/DreamShaperXL_v21TurboDPMSDE.safetensors
```

**Option 3: Alternative Model (Smaller)**
If you want a smaller model to test:
- **ReV Animated** (2GB): https://civitai.com/models/7371/rev-animated
- Save to: `~/Documents/ComfyUI/models/checkpoints/revAnimated_v122.safetensors`

---

## Current Status

- ✅ AnimateDiff: Ready
- ❌ Main Checkpoint: Need to download

**You can start ComfyUI now**, but you won't be able to generate images until the main checkpoint is downloaded.

---

## Quick Commands

**Check what's downloaded:**
```bash
ls -lh ~/Documents/ComfyUI/models/checkpoints/
ls -lh ~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/
```

**After downloading DreamShaper XL:**
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

