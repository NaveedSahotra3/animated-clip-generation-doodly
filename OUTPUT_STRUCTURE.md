# Output Structure & Naming

## 📁 New Output Directory Structure

```
output/
  └── survival/
      └── images/
          ├── scene-1.png
          ├── scene-2.png
          ├── scene-3.png
          └── ...
```

## 🏷️ Image Naming

Images are now named sequentially based on their order in the prompts file:
- **First prompt** → `scene-1.png`
- **Second prompt** → `scene-2.png`
- **Third prompt** → `scene-3.png`
- And so on...

The numbering is **automatic** - just add prompts to the file in the order you want them numbered.

---

## 📝 Where to Add Prompts

**File:** `templates/youtube_sketch_prompts.txt`

This file controls:
1. **Which prompts** are generated
2. **The order** they appear (determines scene numbers)
3. **The content** of each prompt

### Format Example:

```
prompt_name_1:
Your first prompt description here.

prompt_name_2:
Your second prompt description here.

prompt_name_3:
Your third prompt description here.
```

**The order in the file = the scene number!**

---

## 🚀 Usage

### Generate All Scenes

```bash
python3 scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --parallel 2 \
  --steps 20
```

**Output:** All images saved to `output/survival/images/` as `scene-1.png`, `scene-2.png`, etc.

### Custom Output Directory

```bash
python3 scripts/batch_generate_sketches.py \
  --file templates/youtube_sketch_prompts.txt \
  --output output/my_custom_folder/images
```

---

## 📋 Current Prompt Order

Based on `templates/youtube_sketch_prompts.txt`:

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

## ✏️ How to Reorder Scenes

1. Open `templates/youtube_sketch_prompts.txt`
2. Move prompt blocks to the desired order
3. Run the batch script again
4. Images will be renumbered automatically

**Example:** If you move `fear_paralysis` to the first position, it will become `scene-1.png`

---

## ➕ How to Add New Scenes

1. Open `templates/youtube_sketch_prompts.txt`
2. Add your new prompt at the end (or wherever you want it):

```
new_scene_name:
Your new prompt description here.
```

3. Save the file
4. Run the batch script
5. New image will be saved as the next scene number (e.g., `scene-11.png`)

---

## 🗑️ How to Remove Scenes

1. Open `templates/youtube_sketch_prompts.txt`
2. Delete the entire prompt block (name + text)
3. Save the file
4. Run the batch script
5. Remaining scenes will be renumbered automatically

---

## 💡 Tips

- **Order matters!** The first prompt in the file becomes `scene-1.png`
- **Prompt names** (before the colon) are just for reference - they don't affect the output filename
- **Empty lines** between prompts are optional but recommended for readability
- **Comments** (lines starting with `#`) are ignored

---

## 📖 More Information

See `HOW_TO_ADD_PROMPTS.md` for detailed instructions on adding and editing prompts.

