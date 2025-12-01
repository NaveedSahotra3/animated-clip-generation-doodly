# Next Steps After Installation

## ✅ Phase 1: Verification (5 minutes)

### Step 1: Test Installation
```bash
cd /Volumes/workspace/animated-clip-generation
python scripts/test_installation.py
```

This will verify:
- ✅ System dependencies (Homebrew, Python, Git)
- ✅ ComfyUI installation
- ✅ Custom nodes (AnimateDiff, Manager)
- ✅ Model files (if downloaded)
- ✅ Python packages
- ✅ Project scripts
- ✅ ComfyUI server status

### Step 2: Download Models (if not done)

```bash
cd ~/Documents/ComfyUI
./download_models.sh
```

**Required Models:**
1. **DreamShaper XL** (6.5GB)
   - URL: https://civitai.com/models/112902/dreamshaper-xl
   - Save to: `~/Documents/ComfyUI/models/checkpoints/`

2. **AnimateDiff Motion Module** (~700MB)
   - URL: https://huggingface.co/guoyww/animatediff/tree/main
   - File: `mm_sd_v15_v2.ckpt`
   - Save to: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

---

## 🎬 Phase 2: First Generation (15 minutes)

### Step 1: Start ComfyUI

**Terminal 1:**
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

Wait for: `Starting server...` and `To see the server go to: http://127.0.0.1:8188`

### Step 2: Open ComfyUI Interface

Open browser: **http://127.0.0.1:8188**

You should see the ComfyUI interface with nodes.

### Step 3: Load Workflow

**Option A: Drag & Drop (Easiest)**
1. Open Finder
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Drag `whiteboard_animation.json` onto ComfyUI browser window

**Option B: Load Button**
1. Click "Load" button (top right in ComfyUI)
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Select `whiteboard_animation.json`

### Step 4: Configure Workflow

1. **Find the CLIPTextEncode node** (positive prompt)
2. **Edit the prompt** to:
   ```
   simple line drawing of a man standing, white background, clean black lines, minimalist sketch, hand drawn style
   ```

3. **Check settings:**
   - Resolution: 768x768
   - Frames: 48 (2 seconds)
   - Steps: 25
   - CFG Scale: 7.5

### Step 5: Generate First Clip

1. Click **"Queue Prompt"** (bottom right)
2. Watch the progress in the queue
3. Wait 5-10 minutes for generation
4. Result will appear in: `~/Documents/ComfyUI/output/`

---

## 🚀 Phase 3: Test Python Scripts (10 minutes)

### Test Single Clip Generation

**Terminal 2** (keep ComfyUI running in Terminal 1):

```bash
cd /Volumes/workspace/animated-clip-generation
python scripts/generate_clip.py \
  --prompt "simple line drawing of a man walking, white background, clean lines" \
  --duration 2 \
  --output test_output
```

**Expected:**
- Connects to ComfyUI API
- Queues generation
- Downloads result
- Saves to `test_output/`

### Test Voiceover Generation

```bash
python scripts/generate_voiceover.py \
  --text "This is a test voiceover" \
  --engine macos \
  --output test_voiceover.wav
```

**Expected:**
- Generates WAV file
- Saves to current directory

---

## 📝 Phase 4: Create Your First Project (30 minutes)

### Step 1: Create Project Structure

```bash
cd /Volumes/workspace/animated-clip-generation
mkdir -p projects/my_first_video/{clips,voiceover,final}
```

### Step 2: Create Script

```bash
cat > projects/my_first_video/script.txt << 'EOF'
Meet John. (2)
John is a friendly person. (3)
John walks to his home. (3)
John arrives home. (2)
EOF
```

### Step 3: Generate Clips

```bash
python scripts/batch_generate.py \
  --script projects/my_first_video/script.txt \
  --output projects/my_first_video/clips
```

**Expected:**
- Generates 4 clips (2s, 3s, 3s, 2s)
- Saves to `projects/my_first_video/clips/`
- Creates `manifest.json`

### Step 4: Generate Voiceover

```bash
python scripts/generate_voiceover.py \
  --text "Meet John. John is a friendly person. John walks to his home. John arrives home." \
  --output projects/my_first_video/voiceover/narration.wav
```

### Step 5: Assemble Video

```bash
# Install ffmpeg if needed
brew install ffmpeg

# Assemble video
python scripts/assemble_video.py \
  --clips projects/my_first_video/clips \
  --voiceover projects/my_first_video/voiceover/narration.wav \
  --output projects/my_first_video/final/video.mp4
```

**Expected:**
- Combines all clips
- Syncs voiceover
- Creates final MP4 file

---

## 🎨 Phase 5: Post-Processing (Optional)

### After Effects / Premiere Pro

1. Import final video
2. Add drawing hand overlay (download from Pixabay)
3. Add transitions
4. Color correction (pure white background)
5. Export: H.264, 1920x1080

---

## 📚 Learning Resources

### Prompt Engineering

See `templates/` directory for:
- `character_prompts.txt` - Character templates
- `scene_prompts.txt` - Scene templates
- `action_prompts.txt` - Action templates

### Workflow Customization

- Edit `workflows/whiteboard_animation.json` for different settings
- Adjust resolution, steps, CFG scale
- Experiment with different samplers

### Advanced Usage

Read documentation:
- `docs/WORKFLOW.md` - Complete workflow guide
- `docs/TROUBLESHOOTING.md` - Common issues
- `QUICKSTART.md` - Quick reference

---

## 🐛 Troubleshooting

### ComfyUI won't start
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16
```

### Models not showing
1. Check files are in correct folders
2. Refresh browser (F5)
3. Restart ComfyUI

### Generation fails
- Check ComfyUI is running
- Verify models are downloaded
- Check console for errors
- Try simpler prompt first

### Python scripts fail
- Ensure ComfyUI is running
- Check API connection: `curl http://127.0.0.1:8188/system_stats`
- Verify Python packages: `pip list`

---

## ✅ Success Checklist

- [ ] Installation test passes
- [ ] Models downloaded
- [ ] ComfyUI starts successfully
- [ ] Workflow loads correctly
- [ ] First clip generated
- [ ] Python scripts work
- [ ] First project completed

---

## 🎯 What's Next?

1. **Experiment with prompts** - Try different styles
2. **Adjust settings** - Find your quality/speed balance
3. **Build asset library** - Save good clips for reuse
4. **Create templates** - Standardize your workflow
5. **Scale up** - Produce multiple videos

**You're ready to create! 🚀**

