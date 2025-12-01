# How to Add Prompts Sequentially

## 📝 Where to Add Prompts

**File Location:** `templates/youtube_sketch_prompts.txt`

This file contains all your prompts in sequential order. The order in this file determines the scene numbers:
- First prompt → `scene-1.png`
- Second prompt → `scene-2.png`
- Third prompt → `scene-3.png`
- And so on...

---

## ✏️ How to Add/Edit Prompts

### Format

Each prompt follows this format:

```
prompt_name:
Your prompt text here. This can be multiple lines.
Just continue writing on the next line if needed.
```

### Example

```
split_brain_mind:
Split-brain sketch: One half shows a calm, controlled mind (organized thoughts, clear pathways). Other half shows chaos (swirling emotions, fear symbols, anger bursts, depression clouds). A person stands between both halves, deciding which to follow.

fear_paralysis:
Intense sketch of a person's face showing raw fear—wide eyes, sweat, but body frozen in place unable to move. Threats surround them (shadows, danger symbols) but they're paralyzed. Contrast with small inset showing fear used productively (cautious, alert, but still moving).
```

### Rules

1. **Prompt name** (before the colon `:`) must be on its own line
2. **No spaces** before the prompt name
3. **Prompt text** can be multiple lines
4. **Empty lines** between prompts are optional but recommended for readability
5. **Comments** (lines starting with `#`) are ignored

---

## 📋 Step-by-Step: Adding a New Prompt

### Method 1: Add at the End

1. Open `templates/youtube_sketch_prompts.txt`
2. Scroll to the end
3. Add your new prompt:

```
new_prompt_name:
Your new prompt description here. Make it detailed and descriptive.
```

4. Save the file
5. Run the batch script - it will automatically number it as the next scene

### Method 2: Insert in the Middle

1. Open `templates/youtube_sketch_prompts.txt`
2. Find where you want to insert the new prompt
3. Add your prompt (the numbering will automatically adjust)
4. Save the file

**Note:** If you insert a prompt in the middle, all subsequent prompts will be renumbered when you run the batch script.

---

## 🎯 Current Prompt Order

Your prompts are numbered in the order they appear in the file:

1. `split_brain_mind` → `scene-1.png`
2. `fear_paralysis` → `scene-2.png`
3. `anxiety_pacing` → `scene-3.png`
4. `frustration_anger` → `scene-4.png`
5. `depression_darkness` → `scene-5.png`
6. `loneliness_paths` → `scene-6.png`
7. `survivor_guilt` → `scene-7.png`
8. `emotions_demons_tools` → `scene-8.png`
9. `survivor_comparison` → `scene-9.png`
10. `emotions_mastery` → `scene-10.png`

---

## 💡 Tips

1. **Keep prompt names short and descriptive** (they're just for reference)
2. **Order matters** - the first prompt becomes scene-1, second becomes scene-2, etc.
3. **You can have as many prompts as you want** - just add them to the file
4. **To reorder scenes**, just move the prompt blocks in the file
5. **To remove a scene**, delete the entire prompt block (name + text)

---

## 🚀 After Adding Prompts

Run the batch generation:

```bash
python3 scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --parallel 2 \
  --steps 20
```

All images will be saved to: `output/survival/images/` as `scene-1.png`, `scene-2.png`, etc.

---

## 📁 File Structure

```
templates/
  └── youtube_sketch_prompts.txt  ← Edit this file to add/modify prompts

output/
  └── survival/
      └── images/                  ← Generated images go here
          ├── scene-1.png
          ├── scene-2.png
          ├── scene-3.png
          └── ...
```

