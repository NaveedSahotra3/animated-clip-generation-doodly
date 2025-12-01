# Troubleshooting Guide

Common issues and solutions.

## Installation Issues

### Homebrew installation fails

```bash
# Try manual installation
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (M1 Mac)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

### Python 3.10 not found

```bash
# Install via Homebrew
brew install python@3.10

# Verify
python3.10 --version
```

### ComfyUI installation fails

```bash
cd ~/Documents/ComfyUI
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install -r requirements.txt
```

## Runtime Issues

### ComfyUI won't start

**Error: Module not found**
```bash
cd ~/Documents/ComfyUI
source venv/bin/activate
pip install -r requirements.txt
```

**Error: Port already in use**
```bash
# Kill existing process
lsof -ti:8188 | xargs kill -9

# Or use different port
python main.py --port 8189
```

**Error: CUDA/GPU issues**
- M1 Macs use Metal, not CUDA
- Use `--force-fp16` flag (already in launch script)
- Check Activity Monitor for memory usage

### Models not loading

**Model not found**
1. Check file location:
   - Checkpoints: `~/Documents/ComfyUI/models/checkpoints/`
   - AnimateDiff: `~/Documents/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`
2. Check filename matches exactly (case-sensitive)
3. Refresh browser (F5)
4. Restart ComfyUI

**Wrong model format**
- Use `.safetensors` for checkpoints
- Use `.ckpt` for AnimateDiff motion modules
- Verify file isn't corrupted (re-download if needed)

### Generation Issues

**Out of memory**
- Reduce resolution: `--resolution 512x512`
- Lower steps: `--steps 20`
- Close other applications
- Restart ComfyUI

**Slow generation**
- Use `--force-fp16` flag
- Reduce resolution
- Use Turbo models (faster)
- Check Activity Monitor for CPU/GPU usage

**Generation fails**
- Check ComfyUI is running
- Verify model is loaded
- Check API connection: `curl http://127.0.0.1:8188/system_stats`
- Review ComfyUI console for errors

**Inconsistent results**
- Use same seed for related clips: `--seed 12345`
- Use consistent prompts
- Generate all clips in same session
- Consider using LoRA for style consistency

### AnimateDiff Issues

**AnimateDiff not working**
- Verify motion module is downloaded
- Check file is in correct location
- Restart ComfyUI after adding module
- Check workflow includes AnimateDiff nodes

**Video output missing**
- Check workflow has SaveImage/VideoCombine node
- Verify output directory exists
- Check ComfyUI output folder: `~/Documents/ComfyUI/output/`

**Poor animation quality**
- Increase context length (16-32)
- Adjust motion scale (0.5-2.0)
- Use more frames (48+ for 2 seconds)
- Try different motion modules

## Script Issues

### generate_clip.py fails

**Connection error**
```bash
# Check ComfyUI is running
./scripts/start_comfyui.sh

# Test connection
curl http://127.0.0.1:8188/system_stats
```

**Workflow not found**
- Verify workflow file exists: `workflows/whiteboard_animation.json`
- Check file permissions
- Try using basic workflow

### batch_generate.py issues

**Script parsing fails**
- Check script file format (see example)
- Verify file encoding (UTF-8)
- Check line endings (Unix format)

**Clips not generating**
- Check individual clip generation works first
- Review error messages
- Check output directory permissions

### generate_voiceover.py issues

**TTS engine not found**
```bash
# Install Coqui TTS
pip install TTS

# Or use macOS say (default)
python scripts/generate_voiceover.py --engine macos --text "test"
```

**Output file issues**
- Check write permissions
- Verify output directory exists
- Check disk space

### assemble_video.py issues

**ffmpeg not found**
```bash
brew install ffmpeg
```

**Video assembly fails**
- Check all clip files exist
- Verify file formats (MP4 recommended)
- Check file permissions
- Review ffmpeg error messages

**Audio sync issues**
- Verify voiceover duration matches video
- Check audio format (WAV recommended)
- Adjust timing in editing software

## Performance Optimization

### Speed up generation

1. Use Turbo models
2. Reduce steps (20-25)
3. Lower resolution (512x512 for testing)
4. Use FP16 precision (already enabled)
5. Close other applications

### Improve quality

1. Increase steps (30-40)
2. Higher resolution (768x768 or 1024x768)
3. Use quality models (non-Turbo)
4. Fine-tune prompts
5. Use LoRA for style

### Memory management

- Monitor with Activity Monitor
- Restart ComfyUI periodically
- Clear output directory
- Use smaller batch sizes

## Getting Help

1. Check ComfyUI console for errors
2. Review log files
3. Test with simple prompts first
4. Verify all dependencies installed
5. Check system requirements met

## Common Error Messages

**"Model not found"**
→ Check file location and filename

**"Out of memory"**
→ Reduce resolution/steps, close apps

**"Connection refused"**
→ Start ComfyUI server

**"Module not found"**
→ Install missing dependencies

**"Workflow invalid"**
→ Check workflow JSON format

**"Generation timeout"**
→ Increase timeout or check ComfyUI status

