# Troubleshooting Workflow Issues

## ❌ "Missing Models" Dialog - HunyuanVideo Models

**You're seeing:** A dialog asking for HunyuanVideo models (qwen, byt5, hunyuanvideo, etc.)

**Why:** This is from a different workflow that was previously loaded or is still in ComfyUI's memory.

**Solution:**
1. **Close the dialog** - Click the X button or check "Don't show this again"
2. **Clear ComfyUI** - Press `Ctrl+Shift+R` or refresh the browser
3. **Load the correct workflow** - Use `whiteboard_animation.json` from our project

---

## ✅ Correct Workflow Setup

### Step 1: Clear and Reload

1. In ComfyUI browser, press `Ctrl+Shift+R` (or Cmd+Shift+R on Mac) to hard refresh
2. This clears any cached workflows

### Step 2: Load Our Workflow

**Option A: Drag & Drop**
1. Open Finder
2. Go to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Drag `whiteboard_animation.json` onto ComfyUI

**Option B: Load Button**
1. Click "Load" (top right)
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Select: `whiteboard_animation.json`

### Step 3: Verify Model Selection

After loading, check the **CheckpointLoaderSimple** node:
- Should show: `dreamshaperXL_lightningDPMSDE.safetensors`
- If it shows something else, click the dropdown and select your model

### Step 4: Verify AnimateDiff

Check the **AnimateDiffLoaderWithContext** node:
- Should show: `mm_sd_v15_v2.ckpt`
- If missing, it's in: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

---

## 🔧 If Workflow Still Shows Wrong Models

### Manual Fix in ComfyUI:

1. **Find CheckpointLoaderSimple node** (top left)
2. **Click the model dropdown**
3. **Select:** `dreamshaperXL_lightningDPMSDE.safetensors`

4. **Find AnimateDiffLoaderWithContext node**
5. **Click the motion module dropdown**
6. **Select:** `mm_sd_v15_v2.ckpt`

---

## ✅ What You Should See

**Correct workflow should have:**
- ✅ CheckpointLoaderSimple → `dreamshaperXL_lightningDPMSDE.safetensors`
- ✅ AnimateDiffLoaderWithContext → `mm_sd_v15_v2.ckpt`
- ✅ CLIPTextEncode nodes (positive and negative prompts)
- ✅ EmptyLatentImage → 768x768, 48 frames
- ✅ KSampler → 25 steps, 7.5 CFG
- ✅ AnimateDiffCombine
- ✅ SaveImage

**You should NOT see:**
- ❌ UNETLoader
- ❌ DualCLIPLoader
- ❌ HunyuanVideo models
- ❌ Any qwen, byt5, or hunyuanvideo references

---

## 🚀 Quick Fix Steps

```bash
# 1. Stop ComfyUI (Ctrl+C in terminal)

# 2. Restart ComfyUI
cd ~/Documents/ComfyUI
./launch_comfyui.sh

# 3. In browser:
#    - Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
#    - Load workflow: whiteboard_animation.json
#    - Verify model: dreamshaperXL_lightningDPMSDE.safetensors
#    - Click Queue Prompt
```

---

## 📝 Summary

- **HunyuanVideo models are NOT needed** - Close that dialog
- **Use our workflow:** `whiteboard_animation.json`
- **Model name:** `dreamshaperXL_lightningDPMSDE.safetensors`
- **Motion module:** `mm_sd_v15_v2.ckpt`

If you still see errors, the workflow file has been updated with the correct model name. Reload it!

