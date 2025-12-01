# How to Export Workflow from ComfyUI

## ❌ What You Copied

The file `ComfyUI_Workflow_v1.0.json` is a **JSON schema definition**, not an actual workflow. That's why it's not working.

## ✅ How to Export the Actual Workflow

### Method 1: Save Button (Recommended)

1. **In ComfyUI browser:**
   - Build your workflow (or load an existing one)
   - Click **"Save"** button (top menu, next to "Load")
   - Save as: `my_workflow.json`
   - This saves the actual workflow with all nodes and connections

### Method 2: Download from Browser

1. **In ComfyUI:**
   - Right-click on the canvas (or press `Ctrl+S` / `Cmd+S`)
   - Select "Save" or "Download"
   - This downloads the workflow JSON

### Method 3: Copy from API

If you want to get it programmatically:
```bash
curl http://127.0.0.1:8188/prompt > workflow.json
```

---

## 🔧 Fix Current Workflow in ComfyUI

Instead of exporting, let's fix what you have:

### Step 1: Clear Everything
- Press `Ctrl+A` (or `Cmd+A` on Mac)
- Press `Delete`

### Step 2: Load Our Simple Workflow
1. Click "Load"
2. Select: `workflows/whiteboard_animation.json`
3. This should load without errors

### Step 3: Verify Model
- Check the **CheckpointLoaderSimple** node
- Should show: `dreamshaperXL_lightningDPMSDE.safetensors`
- If not, click dropdown and select it

### Step 4: Test Generation
- Click "Queue Prompt"
- Should work now!

---

## 📝 What a Real Workflow Looks Like

A real workflow JSON should have:
- `"nodes"` array with actual node data
- `"links"` array with connections
- `"widgets_values"` with actual values
- NOT `"$ref"` or `"definitions"` (those are schema)

Example structure:
```json
{
  "last_node_id": 7,
  "last_link_id": 9,
  "nodes": [
    {
      "id": 1,
      "type": "CheckpointLoaderSimple",
      "widgets_values": ["dreamshaperXL_lightningDPMSDE.safetensors"],
      ...
    }
  ],
  "links": [...]
}
```

---

## 🚀 Quick Solution

**Just use the workflow I created:**

1. In ComfyUI, click "Load"
2. Select: `/Volumes/workspace/animated-clip-generation/workflows/whiteboard_animation.json`
3. It should load and work immediately!

This workflow is already configured with your models and should work without errors.

