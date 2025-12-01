# Troubleshooting ComfyUI 500 Error

## Current Issue
ComfyUI is returning 500 errors when trying to process the workflow via API.

## Quick Fix - Use ComfyUI Web Interface

1. **Open ComfyUI in browser:**
   ```bash
   open http://127.0.0.1:8188
   ```

2. **Load the workflow manually:**
   - Click "Load" button
   - Select: `workflows/basic_image.json`
   - Check for any error messages in the interface

3. **If workflow loads successfully:**
   - The issue is with the API request format
   - Try generating one image manually in the web interface
   - Then export the workflow again to get the correct format

4. **If workflow fails to load:**
   - Check the error message in ComfyUI
   - The workflow structure might need adjustment

## Alternative: Use Single Image Script

Instead of batch processing, generate images one at a time:

```bash
# Generate one image at a time
for prompt in "split_brain_mind" "fear_paralysis" "anxiety_pacing"; do
  python3 scripts/generate_sketch_image.py \
    --prompt "$(grep -A1 "^${prompt}:" templates/youtube_sketch_prompts.txt | tail -1)" \
    --steps 20
  sleep 10
done
```

## Check ComfyUI Logs

ComfyUI logs might show the actual error:

```bash
# Check if ComfyUI is writing to stdout
# Look at the terminal where you started ComfyUI
# Or check for log files in ~/Documents/ComfyUI/
```

## Next Steps

1. Open ComfyUI web interface and check for errors
2. Try loading the workflow manually
3. If it works in web interface, the API format might be wrong
4. If it doesn't work, we need to fix the workflow structure

