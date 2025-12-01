# Step-by-Step Installation Guide

## 🎬 Quick Installation (Recommended)

### Step 1: Open Terminal
Press `Cmd + Space`, type "Terminal", press Enter

### Step 2: Navigate to Project Directory
```bash
cd /Volumes/workspace/animated-clip-generation
```

### Step 3: Run Installation
```bash
# Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# Run installation
./scripts/install.sh
```

### Step 4: Wait for Installation
This will take 15-20 minutes. You'll see progress messages. When it says "✅ Installation Complete!", continue.

### Step 5: Download Models
```bash
cd ~/Documents/ComfyUI
./download_models.sh
```

This will show you 2 download links. Open them in your browser:

**Model 1: DreamShaper XL**
- Go to: https://civitai.com/models/112902/dreamshaper-xl
- Click "Download" button
- Move downloaded file to: `~/Documents/ComfyUI/models/checkpoints/`

**Model 2: AnimateDiff Motion**
- Go to: https://huggingface.co/guoyww/animatediff/tree/main
- Click on `mm_sd_v15_v2.ckpt`
- Click download icon
- Move to: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

### Step 6: Launch ComfyUI
```bash
cd ~/Documents/ComfyUI
./launch_comfyui.sh
```

Open browser and go to: **http://127.0.0.1:8188**

### Step 7: Load Animation Workflow

Once ComfyUI interface loads:

1. Click "Load" button (top right)
2. Navigate to: `/Volumes/workspace/animated-clip-generation/workflows/`
3. Select: `whiteboard_animation.json`
4. Edit the positive prompt to: `"animated sketch of man walking, white background, clean lines"`
5. Click "Queue Prompt" (bottom right)
6. Wait 5-10 minutes for your first animation!

---

## 🚨 Troubleshooting

### Homebrew installation asks for password?
Enter your Mac password (it won't show while typing)

### Python errors?
```bash
brew install python@3.10
python3.10 --version
```

### Git clone fails?
Check your internet connection and try again

### ComfyUI won't start?
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
python main.py --force-fp16
```

### Models not showing?
1. Check files are in correct folders
2. Refresh browser (F5)
3. Restart ComfyUI

---

## ✅ Verification

After installation, you should have:

- ✅ ComfyUI installed at `~/Documents/ComfyUI`
- ✅ Helper scripts in ComfyUI directory:
  - `launch_comfyui.sh`
  - `download_models.sh`
  - `generate_voiceover.sh`
- ✅ Project scripts in `/Volumes/workspace/animated-clip-generation/scripts/`
- ✅ Models downloaded (DreamShaper XL + AnimateDiff)

---

## Next Steps

1. Generate your first clip using the workflow
2. Read `docs/WORKFLOW.md` for detailed usage
3. Try batch generation: `python scripts/batch_generate.py --help`
4. Create your first project!

