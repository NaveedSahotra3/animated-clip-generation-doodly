# AI Whiteboard Video Generator - M1 Max 32GB Setup

## Your System Advantage
With M1 Max 32GB, you can:
- Run SDXL models smoothly
- Generate higher resolution (1024x1024)
- Batch process multiple clips
- Use AnimateDiff without issues

---

## Phase 1: Installation (30 minutes)

### Step 1: Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Dependencies
```bash
brew install python@3.10 git wget
```

### Step 3: Install ComfyUI
```bash
cd ~/Documents
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install -r requirements.txt
```

### Step 4: Install ComfyUI Manager (Essential)
```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..
```

### Step 5: Install AnimateDiff
```bash
cd custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
cd ..
```

---

## Phase 2: Download Models (1-2 hours)

### Directory Structure
```
ComfyUI/
├── models/
│   ├── checkpoints/          # Main models
│   ├── loras/                # Style modifiers
│   ├── controlnet/           # Control models
│   └── animatediff_models/   # Motion models
```

### Essential Models to Download

#### 1. Main Checkpoint (Choose One)

**Option A: DreamShaper XL (Recommended for your system)**
- URL: https://civitai.com/models/112902/dreamshaper-xl
- Download: `DreamShaperXL_v21TurboDPMSDE.safetensors`
- Size: ~6.5GB
- Save to: `ComfyUI/models/checkpoints/`
- Best for: Cartoon/sketch style, fast generation

**Option B: ReV Animated (Alternative)**
- URL: https://civitai.com/models/7371/rev-animated
- Download: `revAnimated_v122.safetensors`
- Size: ~2GB
- Save to: `ComfyUI/models/checkpoints/`
- Best for: Anime/cartoon style

#### 2. AnimateDiff Motion Module

**Download:**
- URL: https://huggingface.co/guoyww/animatediff/tree/main
- File: `mm_sd_v15_v2.ckpt` or `mm_sdxl_v10_beta.ckpt`
- Save to: `ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

#### 3. LoRA for Sketch Style

**Sketch/Line Art LoRA:**
- Search on Civitai: "sketch style" or "line art"
- Recommended: "Sketch Style LoRA" or "Hand Drawn Style"
- Size: ~100-300MB
- Save to: `ComfyUI/models/loras/`

### Quick Download Commands

Create download script:
```bash
cd ~/Documents/ComfyUI
mkdir -p models/checkpoints models/loras
cd models/checkpoints

# Download DreamShaper XL (you'll need to get the direct link from Civitai)
# Use browser to download, then move to this folder
```

---

## Phase 3: First Run & Test (15 minutes)

### Start ComfyUI
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16
```

### Access Interface
Open browser: http://127.0.0.1:8188

### Test Generation
1. You'll see a default workflow
2. Click "Queue Prompt" (bottom right)
3. Should generate an image in ~30 seconds

**If it works, you're ready to proceed!**

---

## Phase 4: Whiteboard Animation Workflow

### Workflow Setup in ComfyUI

I'll describe the node setup (you can build this or load a pre-made workflow):

#### Basic Image Generation Workflow

**Nodes needed:**
1. **Load Checkpoint** → Select your model
2. **CLIP Text Encode (Prompt)** → Positive prompt
3. **CLIP Text Encode (Prompt)** → Negative prompt
4. **Empty Latent Image** → Set size (768x768)
5. **KSampler** → Generation settings
6. **VAE Decode** → Convert to image
7. **Save Image** → Output

#### AnimateDiff Video Workflow

**Additional nodes:**
1. **AnimateDiff Loader** → Load motion module
2. **AnimateDiff Combine** → Create animation
3. **Video Combine** → Export as video

### Optimized Settings for M1 Max 32GB

**Generation Settings:**
- Resolution: 768x768 (characters) or 1024x768 (scenes)
- Steps: 25-30
- CFG Scale: 7-8
- Sampler: DPM++ 2M Karras or Euler A
- Scheduler: Karras
- Batch Size: 1 (for video) or 4 (for images)

**AnimateDiff Settings:**
- Frame Count: 48 (2 seconds at 24fps) or 96 (4 seconds)
- Context Length: 16
- Motion Scale: 1.0

---

## Phase 5: Prompt Engineering for Whiteboard Style

### Character Generation Prompts

**Template:**
```
Positive: "simple line drawing, sketch, character [description], white background, clean black lines, minimalist style, hand drawn, children's book illustration, single character, full body"

Negative: "colored, photo realistic, complex, detailed background, shadows, gradients, multiple characters, blurry, low quality"
```

**Examples:**

**Character - John:**
```
Positive: "simple line drawing sketch of a young man named John, full body, white background, clean black lines, minimalist cartoon style, friendly expression, standing pose, hand drawn"

Negative: "colored, photo realistic, complex background, shadows, multiple people"
```

**Object - House:**
```
Positive: "simple line drawing of a small house, white background, clean black lines, minimalist style, front view, hand drawn sketch, children's book illustration"

Negative: "colored, realistic, complex, detailed, shadows, perspective"
```

**Action - John Walking:**
```
Positive: "simple line drawing of a man walking, side view, white background, clean black lines, minimalist animation style, motion lines, hand drawn sketch"

Negative: "colored, static, complex, realistic"
```

### Animation Prompts (with AnimateDiff)

Add motion descriptions:
```
Positive: "animated sketch of [character/action], smooth movement, hand drawn animation, white background, clean lines, simple motion"
```

---

## Phase 6: Production Workflow

### Step-by-Step Video Creation

**Project: "Then John goes to home"**

#### A. Generate Clips (in ComfyUI)

**Clip 1: John Standing (2 sec)**
- Prompt: "simple line drawing of young man John standing, white background, clean lines"
- Frames: 48
- Output: `john_standing.mp4`

**Clip 2: House Appears (2 sec)**  
- Prompt: "simple line drawing of house appearing, white background, clean lines, minimalist"
- Frames: 48
- Output: `house_appear.mp4`

**Clip 3: John Walking (3 sec)**
- Prompt: "animated sketch of man walking toward house, side view, white background, motion"
- Frames: 72
- Output: `john_walking.mp4`

**Generation Time: ~5-10 minutes per clip**

#### B. Export from ComfyUI
- All videos saved in `ComfyUI/output/`
- Format: MP4 or PNG sequence

#### C. Edit in Premiere Pro / After Effects

**After Effects Method (Better for drawing effect):**

1. **Import clips**
   - File → Import → Your generated videos

2. **Create composition**
   - 1920x1080, 24fps

3. **Add clips to timeline**
   - Arrange according to script timing

4. **Add drawing effect:**
   - Effect → Generate → Scribble
   - Or Effect → Generate → Stroke
   - Animate these effects to reveal progressively

5. **Add drawing hand overlay:**
   - Download free hand animations from Pixabay
   - Place above your clips
   - Use blend modes to integrate

6. **Add voiceover:**
   - Import audio
   - Sync with visual timing

7. **Export:**
   - Composition → Add to Render Queue
   - Format: H.264, 1920x1080

**Premiere Pro Method (Simpler):**

1. **Create sequence:** 1920x1080, 24fps
2. **Import all clips** to timeline
3. **Add transitions** between scenes
4. **Add voiceover** track
5. **Add drawing hand overlay** videos
6. **Color correction** (if needed) - make backgrounds pure white
7. **Export:** H.264, high quality

---

## Phase 7: Voiceover Generation (Local & Free)

### Option A: Coqui TTS (Better quality)

**Install:**
```bash
pip install TTS
```

**Generate voice:**
```bash
tts --text "Then John goes to home" \
    --model_name tts_models/en/ljspeech/tacotron2-DDC \
    --out_path voiceover.wav
```

**Available voices:**
```bash
tts --list_models
```

### Option B: Piper TTS (Faster)

**Install:**
```bash
pip install piper-tts
```

**Download voice:**
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
```

**Generate:**
```bash
echo "Then John goes to home" | piper \
  --model en_US-lessac-medium.onnx \
  --output_file voiceover.wav
```

### Option C: macOS Built-in (Quick & Easy)

```bash
say -o voiceover.aiff "Then John goes to home"
```

Then convert to WAV in After Effects/Premiere

---

## Phase 8: Complete Example Project

### Project Structure
```
whiteboard_project/
├── script.txt
├── generated_clips/
│   ├── john_standing.mp4
│   ├── house_appear.mp4
│   └── john_walking.mp4
├── voiceover/
│   └── narration.wav
├── assets/
│   └── drawing_hand_overlay.mp4
└── final_export/
    └── final_video.mp4
```

### Script Breakdown

**Full Script:**
```
"Meet John. (2 sec)
John is a friendly guy who loves his home. (3 sec)
One day, John decides to go back home. (3 sec)
He walks down the familiar street. (3 sec)
And finally, John arrives at his beautiful home. (4 sec)"

Total: 15 seconds
```

**Clips Needed:**
1. John character introduction (2s)
2. John smiling (3s)
3. John starting to walk (3s)
4. John walking (3s)
5. John arriving at house (4s)

**Generation time:** 30-45 minutes total
**Editing time:** 30-45 minutes
**Total:** ~1.5 hours for 15-second video

---

## Phase 9: Optimization Tips for M1 Max

### Speed Optimizations

**In ComfyUI:**
```bash
# Use all your CPU cores
python main.py --force-fp16 --preview-method auto
```

**Settings to adjust:**
- Use FP16 precision (already enabled with flag)
- Enable "Auto-Queue" in ComfyUI Manager
- Use "Turbo" models (DreamShaper XL Turbo)

### Quality vs Speed Trade-offs

**Fast (10 steps):**
- Use SDXL Turbo models
- Steps: 8-10
- Time: 20-30 sec per frame

**Balanced (25 steps):** ⭐ Recommended
- Steps: 20-25
- Time: 1-2 min per clip
- Quality: Very good

**High Quality (50 steps):**
- Steps: 40-50
- Time: 3-5 min per clip
- Quality: Excellent

### Memory Management

Your 32GB is plenty, but good practices:
- Close other apps during generation
- Use Activity Monitor to check memory
- Clear ComfyUI cache occasionally (in UI settings)

---

## Phase 10: Troubleshooting

### Common Issues

**1. "Model not found"**
- Check file is in correct folder
- Refresh ComfyUI (F5)
- Check filename matches exactly

**2. "Out of memory"**
- Reduce resolution to 512x512
- Lower batch size to 1
- Restart ComfyUI

**3. "Slow generation"**
- Use `--force-fp16` flag
- Switch to smaller model (SD 1.5)
- Reduce steps to 20

**4. "AnimateDiff not working"**
- Check motion module is downloaded
- Must be in `custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`
- Restart ComfyUI after adding

**5. "Videos look different/inconsistent"**
- Use same seed for related clips
- Use LoRA for consistent style
- Generate all clips in same session

---

## Phase 11: Pre-made Workflows

### Where to Find Workflows

1. **ComfyUI Workflows**: https://comfyworkflows.com
2. **OpenArt**: https://openart.ai/workflows
3. **CivitAI**: Has workflow section

### Importing Workflows

1. Download `.json` workflow file
2. In ComfyUI: Load button (top right)
3. Select your downloaded workflow
4. Install any missing custom nodes (ComfyUI Manager will prompt)

### Recommended Workflows to Try

- "AnimateDiff Simple" - Basic animation
- "Character Consistent Generation" - Same character across frames
- "Sketch to Animation" - Line art animation

---

## Quick Reference Commands

### Daily Usage

**Start ComfyUI:**
```bash
cd ~/Documents/ComfyUI && source venv/bin/activate && python main.py --force-fp16
```

**Update ComfyUI:**
```bash
cd ~/Documents/ComfyUI
git pull
pip install -r requirements.txt --upgrade
```

**Update Custom Nodes:**
Use ComfyUI Manager interface (Update All)

---

## Time Investment Summary

### Initial Setup
- Installation: 30 min
- Model downloads: 1-2 hours
- Testing: 30 min
- **Total: 2-3 hours**

### Per Video (after practice)
- Script writing: 10 min
- Clip generation: 30-45 min
- Video editing: 30-45 min
- **Total: 1-1.5 hours per video**

### Learning Curve
- Day 1: Setup + basic generation
- Day 2: AnimateDiff + first animation
- Day 3: Full video workflow
- Day 4-5: Practice and refinement
- **Week 1: Producing quality videos**

---

## Next Steps

1. **Today:** 
   - Install ComfyUI
   - Download DreamShaper XL
   - Generate first test image

2. **Tomorrow:**
   - Install AnimateDiff
   - Generate first 2-second clip
   - Test prompt variations

3. **Day 3:**
   - Create full 10-15 second video
   - Practice editing in After Effects
   - Experiment with styles

4. **Day 4+:**
   - Refine workflow
   - Build asset library
   - Start producing content

---

## Resources

- **ComfyUI Wiki**: https://github.com/comfyanonymous/ComfyUI/wiki
- **AnimateDiff Guide**: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
- **Model Repository**: https://civitai.com
- **Free Assets**: https://pixabay.com (for hand overlays)
- **Voiceover**: Coqui TTS documentation

---

## Summary

**What you'll achieve:**
- Generate custom whiteboard-style animated clips
- 2-4 seconds per clip
- Full control over characters and scenes
- Edit and assemble in Premiere/After Effects
- Professional quality results
- **Total cost: $0**

**Your M1 Max advantage:**
- Fast generation (1-2 min per clip)
- Can handle SDXL quality
- Smooth AnimateDiff playback
- No VRAM limitations

Ready to start? Begin with Phase 1 installation! 🚀

before implementation let me know if you get it