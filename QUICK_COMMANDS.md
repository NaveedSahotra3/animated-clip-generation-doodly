# 🚀 Quick Commands - YouTube Sketch Generation

## ⚡ FASTEST WAY (Recommended)

```bash
# Generate all 10 sketches in parallel (fastest)
python scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --parallel 2 \
  --steps 20
```

**Time:** ~10-12 minutes | **Quality:** Excellent for YouTube

---

## 📋 All Commands

### 1. Generate All Sketches (Balanced - Best Choice)
```bash
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --parallel 2
```

### 2. Generate All Sketches (Fast Preview)
```bash
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --steps 15 --parallel 2
```

### 3. Generate All Sketches (High Quality)
```bash
python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --steps 30 --parallel 2
```

### 4. Generate Single Sketch (Test)
```bash
python scripts/generate_sketch_image.py \
  --prompt "Split-brain sketch: One half shows a calm, controlled mind" \
  --steps 20 \
  --resolution 1024x768
```

### 5. Start ComfyUI (Required First)
```bash
./scripts/start_comfyui.sh
```

---

## 📊 Speed Comparison

| Mode | Steps | Parallel | Time | Quality |
|------|-------|----------|------|---------|
| Fast | 15 | 2 | ~6-8 min | Good |
| **Balanced** | **20** | **2** | **~10-12 min** | **Excellent** |
| Quality | 30 | 2 | ~18-25 min | Maximum |
| HD | 25 | 1 | ~25-35 min | HD Ready |

---

## 📁 Output Location

All images saved to: `output/youtube_sketches/`

---

## ✅ Checklist Before Running

- [ ] ComfyUI is running (`./scripts/start_comfyui.sh`)
- [ ] Models are downloaded (check with `./scripts/verify_models.sh`)
- [ ] You're in project root directory

---

## 🆘 If Something Goes Wrong

1. **ComfyUI not responding**: Restart it
2. **Out of memory**: Use `--parallel 1` instead of 2
3. **Too slow**: Reduce `--steps` to 15
4. **Quality not good**: Increase `--steps` to 30

