# Quick Fix - Workflow Issues

## Current Issue

The workflow JSON is having compatibility issues. Here's the simplest solution:

## ✅ Solution: Build Workflow in ComfyUI (Easiest)

Instead of loading a complex JSON, let's build it step by step in ComfyUI:

### Step 1: Start Fresh

1. In ComfyUI, press `Ctrl+A` (or Cmd+A on Mac) to select all nodes
2. Press `Delete` to clear everything
3. You should have a blank canvas

### Step 2: Add Nodes (Right-click → Add Node)

**Node 1: CheckpointLoaderSimple**
- Right-click → Add Node → Loaders → CheckpointLoaderSimple
- Select model: `dreamshaperXL_lightningDPMSDE.safetensors`

**Node 2: CLIPTextEncode (Positive)**
- Right-click → Add Node → Conditioning → CLIPTextEncode
- Connect: CheckpointLoaderSimple CLIP output → CLIPTextEncode CLIP input
- Set prompt: `simple line drawing, sketch, white background, clean black lines, minimalist style, hand drawn`

**Node 3: CLIPTextEncode (Negative)**
- Right-click → Add Node → Conditioning → CLIPTextEncode
- Connect: CheckpointLoaderSimple CLIP output → CLIPTextEncode CLIP input
- Set prompt: `colored, realistic, complex background, shadows, multiple characters`

**Node 4: EmptyLatentImage**
- Right-click → Add Node → latent → EmptyLatentImage
- Set: Width 768, Height 768, Batch 48 (for 2 seconds at 24fps)

**Node 5: AnimateDiffLoaderWithContext**
- Right-click → Add Node → AnimateDiff → AnimateDiffLoaderWithContext
- Connect: CheckpointLoaderSimple MODEL output → AnimateDiffLoaderWithContext model input
- Select motion module: `mm_sd_v15_v2.ckpt`
- Set context_length: 16, motion_scale: 1.0

**Node 6: KSampler**
- Right-click → Add Node → Sampling → KSampler
- Connect:
  - AnimateDiffLoaderWithContext MODEL → KSampler model
  - CLIPTextEncode (positive) CONDITIONING → KSampler positive
  - CLIPTextEncode (negative) CONDITIONING → KSampler negative
  - EmptyLatentImage LATENT → KSampler latent_image
- Settings: seed 12345, steps 25, cfg 7.5, sampler "dpmpp_2m", scheduler "karras"

**Node 7: VAEDecode**
- Right-click → Add Node → VAE → VAEDecode
- Connect:
  - KSampler LATENT → VAEDecode samples
  - CheckpointLoaderSimple VAE → VAEDecode vae

**Node 8: AnimateDiffCombine**
- Right-click → Add Node → AnimateDiff → AnimateDiffCombine
- Connect: VAEDecode IMAGE → AnimateDiffCombine images

**Node 9: SaveImage**
- Right-click → Add Node → Image → SaveImage
- Connect: AnimateDiffCombine IMAGE → SaveImage images

### Step 3: Generate

Click "Queue Prompt" (bottom right)

---

## Alternative: Use Basic Image Workflow First

I've created a simpler workflow (`whiteboard_animation.json`) that generates static images first. This will work immediately:

1. Load: `workflows/whiteboard_animation.json`
2. It will generate 48 frames (but as separate images)
3. Once this works, we can add AnimateDiff manually

---

## Why This Happens

ComfyUI workflow JSONs can be version-specific. Building in the UI ensures compatibility.

---

## After Building

Once your workflow works:
1. Click "Save" (top menu)
2. Save as: `my_whiteboard_workflow.json`
3. You can reuse this workflow later

