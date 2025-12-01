# ComfyUI Workflow Usage Guide

## Files You Have

1. **`whiteboard_sketch_workflow.json`** - Static image generation
2. **`animatediff_animation_workflow.json`** - 2-4 second animated clips
3. This guide

---

## Step 1: Import Workflows into ComfyUI

### Method A: Drag and Drop (Easiest)
1. Launch ComfyUI: `./launch_comfyui.sh`
2. Open browser: http://127.0.0.1:8188
3. Drag the `.json` file directly onto the ComfyUI interface
4. Workflow will load automatically

### Method B: Load Button
1. Click "Load" button (top menu)
2. Select the workflow JSON file
3. Click Open

---

## Step 2: Using the Static Image Workflow

### What It Does
Generates single sketch-style images (characters, objects, scenes)

### How to Use

**1. Check Model is Loaded**
- Look at the "CheckpointLoaderSimple" node (top left)
- Should show: `DreamShaperXL_v21TurboDPMSDE.safetensors`
- If missing, download the model first

**2. Edit the Positive Prompt**
Click on the text box in "CLIPTextEncode (Positive)" node

**Example Prompts:**

**Character - John:**
```
simple line drawing of young man John, full body, standing pose, white background, clean black lines, minimalist cartoon style, hand drawn sketch, friendly expression
```

**Object - House:**
```
simple line drawing of small house, white background, clean black lines, minimalist style, front view, hand drawn sketch, simple architecture
```

**Scene - Park:**
```
simple line drawing of park with trees and bench, white background, clean black lines, minimalist sketch, hand drawn style, simple composition
```

**3. Adjust Settings (Optional)**

In the "KSampler" node:
- **seed**: Keep as `fixed` for reproducibility, or change number for variation
- **steps**: 25-30 (higher = better quality but slower)
- **cfg**: 7-8 (how closely to follow prompt)
- **sampler**: `dpmpp_2m` (good default)
- **scheduler**: `karras` (smooth results)

**4. Set Resolution**

In "EmptyLatentImage" node:
- Default: 768x768
- For wider scenes: 1024x768
- For tall characters: 768x1024

**5. Generate**
- Click "Queue Prompt" button (bottom right)
- Wait 1-2 minutes
- Image appears in preview and saves to `ComfyUI/output/`

---

## Step 3: Using the AnimateDiff Workflow

### What It Does
Generates 2-4 second animated clips with motion

### How to Use

**1. Check Required Files**
- Checkpoint model: loaded in top node
- AnimateDiff motion module: `mm_sd_v15_v2.ckpt`
  - Must be in: `custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

**2. Edit Prompts**

**For Character Animation:**
```
Positive: animated sketch of man John waving hand, white background, smooth motion, clean black lines, hand drawn animation, simple movement, character animation

Negative: colored, static, photo realistic, complex background, 3d, detailed
```

**For Walking:**
```
Positive: animated sketch of person walking, side view, white background, smooth walking cycle, clean lines, hand drawn animation, 2d animation style

Negative: colored, static, complex, realistic, multiple people
```

**For Object Appearing:**
```
Positive: house being drawn, progressive reveal, white background, drawing animation, sketch style, line art appearing

Negative: colored, complete, static, realistic, complex
```

**3. Set Frame Count**

In "EmptyLatentImage" node, change the THIRD number (batch size):
- **48 frames** = 2 seconds at 24fps
- **72 frames** = 3 seconds
- **96 frames** = 4 seconds

**4. Adjust Animation Settings**

In "ADE_AnimateDiffUniformContextOptions" node:
- **context_length**: 16 (default, smooth motion)
- **context_overlap**: 4 (smooth transitions)
- Keep other settings as default

**5. Generate Video**
- Click "Queue Prompt"
- Wait 5-10 minutes (longer than static images)
- Video saves to: `ComfyUI/output/whiteboard_animation_XXXXX.mp4`

---

## Step 4: Prompt Engineering Tips

### Structure Your Prompts

**Format:**
```
[art style] + [subject] + [action/pose] + [background] + [quality modifiers]
```

**Good Examples:**
```
✓ "simple line drawing of cat sitting, white background, clean black lines, minimalist sketch"

✓ "animated sketch of bird flying, white background, smooth wing movement, hand drawn animation"

✓ "line art of coffee cup, white background, clean lines, simple illustration"
```

**Avoid:**
```
✗ "a really nice drawing of a cat that looks good"
✗ "photorealistic detailed cat with fur"
✗ Too vague or too complex descriptions
```

### Key Phrases That Work Well

**For Static Images:**
- "simple line drawing"
- "clean black lines"
- "white background"
- "minimalist sketch"
- "hand drawn"
- "cartoon style"

**For Animations:**
- "animated sketch"
- "smooth motion"
- "hand drawn animation"
- "movement"
- "2d animation style"
- "character animation"

### Negative Prompts (Always Include)
```
colored, photo realistic, complex background, shadows, detailed, gradients, blurry, low quality, watermark, multiple subjects
```

---

## Step 5: Batch Generation Strategy

### For a Complete Video Project

**Example: "John Goes Home" (15 seconds)**

**Generate These Clips:**

1. **john_intro.mp4** (2 sec)
   - Prompt: "animated sketch of man John standing and waving"
   - Frames: 48

2. **john_walking.mp4** (3 sec)
   - Prompt: "animated sketch of man walking forward, side view"
   - Frames: 72

3. **house_appears.mp4** (2 sec)
   - Prompt: "house being drawn, progressive reveal, sketch animation"
   - Frames: 48

4. **john_arrives.mp4** (3 sec)
   - Prompt: "man walking up to house, animated sketch"
   - Frames: 72

**Total Generation Time: 30-40 minutes**

### Workflow:
1. Generate clip 1, save
2. Change prompt for clip 2
3. Change seed number (or keep same for consistency)
4. Generate clip 2
5. Repeat for all clips
6. Import all into Premiere Pro/After Effects

---

## Step 6: Maintaining Character Consistency

### Problem: Character looks different in each clip

### Solutions:

**Method 1: Use Same Seed**
- Keep seed number identical across all clips
- Character will look very similar

**Method 2: Use LoRA**
- Download a character LoRA from CivitAI
- Add "LoRA Loader" node before KSampler
- Maintains consistent character appearance

**Method 3: Reference Images (Advanced)**
- Generate one perfect character image
- Use as reference for all subsequent generations
- Requires ControlNet (more advanced)

---

## Step 7: Troubleshooting

### Issue: Model Not Found
**Solution:**
- Download the model from the link
- Place in correct folder: `ComfyUI/models/checkpoints/`
- Refresh browser (F5)

### Issue: AnimateDiff Not Working
**Solution:**
- Check motion module exists: `custom_nodes/ComfyUI-AnimateDiff-Evolved/models/mm_sd_v15_v2.ckpt`
- Restart ComfyUI
- Check Console for error messages

### Issue: Generation is Slow
**Solution:**
- Reduce steps to 20
- Lower resolution to 512x512
- Close other applications
- Use DreamShaper instead of SDXL

### Issue: Results Don't Match Prompt
**Solution:**
- Increase CFG scale to 8-9
- Add more specific details to prompt
- Improve negative prompt
- Try different seed numbers

### Issue: Colors Appearing (Want B&W Only)
**Solution:**
- Add to negative prompt: "colored, color, vibrant, saturated"
- Add to positive: "black and white, monochrome, line art"
- Use stronger CFG scale

### Issue: Out of Memory
**Solution:**
- Reduce resolution
- Lower batch size (frames)
- Close other apps
- Restart ComfyUI with: `python main.py --force-fp16 --lowvram`

---

## Step 8: Export Settings

### From ComfyUI
- Videos save automatically to: `ComfyUI/output/`
- Format: MP4, H.264
- Already optimized for editing

### Import to After Effects
1. File → Import → Multiple Files
2. Select all generated MP4 clips
3. Create new composition (1920x1080, 24fps)
4. Drag clips to timeline

### Import to Premiere Pro
1. File → Import
2. Select all clips
3. Create sequence (1920x1080, 24fps)
4. Drag clips to timeline

---

## Step 9: Quick Reference Commands

### Generate Single Image
1. Load `whiteboard_sketch_workflow.json`
2. Edit positive prompt
3. Queue Prompt
4. Wait ~1-2 min

### Generate Animation Clip
1. Load `animatediff_animation_workflow.json`
2. Edit positive prompt
3. Set frame count (48/72/96)
4. Queue Prompt
5. Wait ~5-10 min

### Generate Voiceover
```bash
./generate_voiceover.sh "Your text here" output.wav
```

### Launch ComfyUI
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

---

## Step 10: Production Timeline

### Day 1: Setup & Testing
- Install everything
- Download models
- Test both workflows
- Generate 2-3 test clips

### Day 2: First Project
- Write 10-second script
- Generate 3-4 clips
- Import to editor
- Practice assembly

### Day 3-4: Full Production
- 30-second video project
- 8-10 clips
- Full edit with voiceover
- Export final video

### Week 2+: Efficient Production
- 1-minute video in 2 hours
- Custom character library
- Template workflows
- Streamlined process

---

## Pro Tips

1. **Build a library** - Save your best character/object generations
2. **Consistent naming** - `projectname_clip01_john_walking.mp4`
3. **Version control** - Keep different seed generations
4. **Batch process** - Generate all clips in one session
5. **Plan ahead** - Storyboard before generating
6. **Reuse assets** - Good characters can be used in multiple videos
7. **Test first** - Always do a quick 2-second test before long clips
8. **Save workflows** - Create custom workflows for different styles

---

## Next Steps

1. ✅ Import workflows into ComfyUI
2. ✅ Test static image generation
3. ✅ Test animation generation
4. ✅ Practice with prompts
5. ✅ Generate your first complete video project

You're ready to start creating! 🎨

**Need help?** Check the Console in ComfyUI (bottom panel) for error messages.