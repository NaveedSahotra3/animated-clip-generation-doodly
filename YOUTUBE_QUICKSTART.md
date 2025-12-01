# YouTube Sketch Generation - Quick Start Guide

## 🚀 Fastest Way to Generate All Your Sketches

### Prerequisites
1. ComfyUI must be running:
   ```bash
   ./scripts/start_comfyui.sh
   ```

2. Wait for ComfyUI to fully load (check http://127.0.0.1:8188)

### Generate All 10 Sketches (Recommended - Fast & Balanced)

```bash

# macbook@MacBooks-MacBook-Pro animated-clip-generation % python3 scripts/batch_generate_sketches.py \
  # --file templates/youtube_sketch_prompts.txt \
  # --parallel 2 \
  # --steps 20

# Sequential (one at a time, most reliable)
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt

# Parallel (2 at a time, faster)
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --parallel 2

# Parallel (3 at a time, fastest but may overload)
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --parallel 3
```

**Expected Time:**
- Sequential: ~15-20 minutes (1.5-2 min per image)
- Parallel (2): ~10-12 minutes
- Parallel (3): ~8-10 minutes

---

## ⚡ Speed vs Quality Options

### Fast Mode (Testing/Quick Preview)
```bash
python scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --steps 15 \
  --parallel 2
```
**Time:** ~6-8 minutes | **Quality:** Good for preview

### Balanced Mode (Recommended for YouTube)
```bash
python scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --steps 20 \
  --parallel 2 \
  --resolution 1024x768
```
**Time:** ~10-12 minutes | **Quality:** Excellent for YouTube

### High Quality Mode (Best Results)
```bash
python scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --steps 30 \
  --cfg 7.5 \
  --parallel 2
```
**Time:** ~18-25 minutes | **Quality:** Maximum quality

### HD Mode (1920x1080 for YouTube)
```bash
python scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --steps 25 \
  --resolution 1920x1080 \
  --parallel 1
```
**Time:** ~25-35 minutes | **Quality:** HD ready

---

## 📝 Generate Single Image

For testing or individual images:

```bash
python scripts/generate_sketch_image.py \
  --prompt "Split-brain sketch: One half shows a calm, controlled mind (organized thoughts, clear pathways). Other half shows chaos (swirling emotions, fear symbols, anger bursts, depression clouds). A person stands between both halves, deciding which to follow." \
  --style sketch \
  --steps 20 \
  --resolution 1024x768
```

---

## 🎯 Your 10 Prompts (Already Configured)

All your prompts are saved in `templates/youtube_sketch_prompts.txt`:

1. `split_brain_mind` - Split-brain decision sketch
2. `fear_paralysis` - Fear and paralysis contrast
3. `anxiety_pacing` - Anxiety pacing with thought bubbles
4. `frustration_anger` - Frustration building to anger
5. `depression_darkness` - Depression and hopelessness
6. `loneliness_paths` - Loneliness with two paths
7. `survivor_guilt` - Survivor's guilt scene
8. `emotions_demons_tools` - Emotions as demons vs tools
9. `survivor_comparison` - Two survivors comparison
10. `emotions_mastery` - Final mastery scene

---

## 📊 Output

All images will be saved to: `output/youtube_sketches/`

Files will be named: `sketch_{prompt_name}_{timestamp}.png`

---

## 🔧 Troubleshooting

### ComfyUI Not Running
```bash
# Start ComfyUI
./scripts/start_comfyui.sh

# Wait for "Starting server" message, then check:
curl http://127.0.0.1:8188/system_stats
```

### Out of Memory Errors
- Reduce `--parallel` to 1
- Reduce `--resolution` to 768x768
- Reduce `--steps` to 15

### Slow Generation
- Check GPU usage (should be high)
- Reduce `--steps` to 15-20
- Use `--parallel 2` instead of 3

### Quality Not Good Enough
- Increase `--steps` to 30
- Increase `--cfg` to 8.0
- Use `--resolution 1024x1024`

---

## 💡 Pro Tips

1. **Start with Fast Mode** to test all prompts work
2. **Use Parallel 2** for best speed/reliability balance
3. **Save seeds** if you want to regenerate specific images
4. **Check first image** before running full batch
5. **HD mode** only if you need 1920x1080 (slower)

---

## 📈 Expected Performance (M1 Max 32GB)

- **Fast (15 steps)**: ~45-60 seconds per image
- **Balanced (20 steps)**: ~1.5-2 minutes per image
- **Quality (30 steps)**: ~2.5-3 minutes per image
- **HD (1920x1080)**: ~3-4 minutes per image

---

## 🎬 Next Steps After Generation

1. Review all images in `output/youtube_sketches/`
2. Regenerate any that need improvement (use same seed)
3. Import into Premiere Pro/After Effects
4. Add voiceover using TTS scripts
5. Assemble final video

---

## 🆘 Need Help?

Check `docs/TROUBLESHOOTING.md` for common issues.

