# 🚀 Start Here - Run Your First Generation

## ✅ Everything is Ready!

All components are installed and models are downloaded. You're ready to generate whiteboard animations!

---

## Step 1: Start ComfyUI Server

**Open Terminal and run:**

```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

**Wait for:**
```
Starting server...
To see the server go to: http://127.0.0.1:8188
```

**Keep this terminal open!** ComfyUI must be running.

---

## Step 2: Open ComfyUI in Browser

Open your browser and go to:
```
http://127.0.0.1:8188
```

You should see the ComfyUI interface with nodes.

---

## Step 3: Load the Whiteboard Animation Workflow

**Option A: Drag & Drop (Easiest)**
1. Open Finder
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Drag `whiteboard_animation.json` onto the ComfyUI browser window

**Option B: Load Button**
1. In ComfyUI, click "Load" button (top right)
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Select: `whiteboard_animation.json`

---

## Step 4: Configure Your First Generation

Once the workflow loads:

1. **Find the CLIPTextEncode node** (positive prompt)
2. **Edit the prompt** to:
   ```
   simple line drawing of a man standing, white background, clean black lines, minimalist sketch, hand drawn style
   ```

3. **Check settings:**
   - Resolution: 768x768
   - Frames: 48 (2 seconds at 24fps)
   - Steps: 25
   - CFG Scale: 7.5

4. **Select your model:**
   - In the CheckpointLoaderSimple node, select: `dreamshaperXL_lightningDPMSDE.safetensors`

---

## Step 5: Generate Your First Clip

1. Click **"Queue Prompt"** button (bottom right)
2. Watch the progress in the queue area
3. Wait 5-10 minutes for generation
4. Result will appear in: `~/Documents/ComfyUI/output/`

---

## 🎬 Alternative: Use Python Scripts

If you prefer command-line:

**Terminal 1: Keep ComfyUI running**
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

**Terminal 2: Generate clip**
```bash
cd /Volumes/workspace/animated-clip-generation
python3.10 scripts/generate_clip.py \
  --prompt "simple line drawing of a man standing, white background, clean lines" \
  --duration 2 \
  --output test_output
```

---

## 📝 Create a Complete Video Project

### 1. Create Script File

```bash
cd /Volumes/workspace/animated-clip-generation
cat > my_script.txt << 'EOF'
Meet John. (2)
John walks to his home. (3)
John arrives home. (2)
EOF
```

### 2. Generate All Clips

```bash
python3.10 scripts/batch_generate.py \
  --script my_script.txt \
  --output projects/my_video/clips
```

### 3. Generate Voiceover

```bash
python3.10 scripts/generate_voiceover.py \
  --text "Meet John. John walks to his home. John arrives home." \
  --engine macos \
  --output projects/my_video/voiceover/narration.wav
```

### 4. Assemble Final Video

```bash
# Install ffmpeg if needed
brew install ffmpeg

# Assemble video
python3.10 scripts/assemble_video.py \
  --clips projects/my_video/clips \
  --voiceover projects/my_video/voiceover/narration.wav \
  --output projects/my_video/final/video.mp4
```

---

## 🎨 Prompt Tips for Whiteboard Style

**Character:**
```
simple line drawing of [character], white background, clean black lines, minimalist sketch, hand drawn style, full body
```

**Action:**
```
animated sketch of [action], white background, motion lines, hand drawn animation, clean lines
```

**Negative prompt (always use):**
```
colored, realistic, complex background, shadows, multiple characters, blurry
```

---

## 📚 Quick Reference

**Start ComfyUI:**
```bash
cd ~/Documents/ComfyUI && ./launch_comfyui.sh
```

**Check models:**
```bash
cd /Volumes/workspace/animated-clip-generation
./scripts/verify_models.sh
```

**View output:**
```bash
ls -lh ~/Documents/ComfyUI/output/
```

**Stop ComfyUI:**
Press `Ctrl+C` in the terminal running ComfyUI

---

## 🐛 Troubleshooting

**ComfyUI won't start?**
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16
```

**Model not showing?**
- Refresh browser (F5)
- Check file is in: `~/Documents/ComfyUI/models/checkpoints/`
- Restart ComfyUI

**Generation fails?**
- Check ComfyUI is running
- Verify model is selected in workflow
- Try simpler prompt first

---

## ✅ You're All Set!

Everything is installed and ready. Start with Step 1 above to generate your first whiteboard animation!

**Happy creating! 🎨**

