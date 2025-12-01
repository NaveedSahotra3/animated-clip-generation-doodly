# Workflow Files Guide

## Available Workflows

### ✅ `whiteboard_animation.json` (USE THIS ONE)
- **Status**: Ready to use
- **Model**: `dreamshaperXL_lightningDPMSDE.safetensors`
- **Type**: Basic image generation (48 frames)
- **How to use**: Load in ComfyUI, click "Queue Prompt"

### ⚠️ `ComfyUI_Workflow_v1.0.json`
- **Status**: This is a JSON schema, NOT a workflow
- **Do not use**: This won't work - it's just a definition file
- **Delete this file** if you want

### 📁 Other Files
- `basic_image.json` - Simple single image generation
- `animatedDiffer-WhiteBoard-animation-workflow.json` - Alternative workflow (may need updates)

---

## How to Use

1. **Start ComfyUI:**
   ```bash
   cd ~/Documents/ComfyUI
   ./launch_comfyui.sh
   ```

2. **Load Workflow:**
   - Open: http://127.0.0.1:8188
   - Click "Load" button
   - Select: `whiteboard_animation.json`

3. **Verify Model:**
   - Check CheckpointLoaderSimple node
   - Should show: `dreamshaperXL_lightningDPMSDE.safetensors`

4. **Generate:**
   - Click "Queue Prompt"
   - Wait for generation

---

## Adding AnimateDiff

After the basic workflow works, you can add AnimateDiff manually:

1. Right-click → Add Node → AnimateDiff → AnimateDiffLoaderWithContext
2. Connect: CheckpointLoaderSimple MODEL → AnimateDiffLoaderWithContext
3. Select: `mm_sd_v15_v2.ckpt`
4. Add AnimateDiffCombine node after VAEDecode
5. Connect everything

See `QUICK_FIX.md` for detailed steps.

