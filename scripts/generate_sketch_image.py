#!/usr/bin/env python3
"""
Generate sketch-based static images using ComfyUI API
Usage: python scripts/generate_sketch_image.py --prompt "your prompt" [options]
"""

import argparse
import json
import requests
import time
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.generation_config import load_config


def queue_prompt(api_url, prompt_workflow):
    """Queue a prompt to ComfyUI API"""
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = requests.post(f"{api_url}/prompt", data=data)
    return req.json()


def get_image(api_url, filename, subfolder, folder_type):
    """Download generated image from ComfyUI"""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url = f"{api_url}/view"
    response = requests.get(url, params=data)
    return response.content


def get_history(api_url, prompt_id):
    """Get generation history"""
    response = requests.get(f"{api_url}/history/{prompt_id}")
    return response.json()


def build_sketch_prompt(user_prompt, style="sketch"):
    """
    Build a complete sketch prompt by combining user prompt with sketch style keywords
    Focused on PENCIL/CHARCOAL style, not digital line art
    
    Args:
        user_prompt: User's base prompt (e.g., "a cat", "young man John")
        style: Style type - "sketch", "character", "object", "scene", "comic"
    """
    # NEW Base keywords - Focused on PENCIL/CHARCOAL, not digital line art
    sketch_base = (
        "rough graphite pencil sketch, charcoal drawing style, "
        "heavy cross-hatching shading, textured paper background, "
        "greyscale, monochrome, intricate details, hand-drawn, "
        "dramatic lighting, gritty atmosphere"
    )
    
    # Style-specific additions
    style_additions = {
        "sketch": "loose gestural lines, storyboard style",
        "character": "character concept art, pencil shading, full body",
        "object": "technical drawing, isolated",
        "scene": "atmospheric perspective, environmental sketch",
        # We redefine comic to avoid 'webtoon' looks
        "comic": "graphic novel storyboard, noir style, dark ink, no text, no speech bubbles"
    }
    
    addition = style_additions.get(style, "")
    
    # Force comic style if requested, but keep it gritty
    if "panel" in user_prompt.lower() or "comic" in user_prompt.lower():
        style = "comic"
        addition = "triptych layout, vertical panels, graphic novel storyboard"
    
    # Combine: base keywords + style addition + user prompt
    if addition:
        full_prompt = f"{sketch_base}, {addition}, {user_prompt}"
    else:
        full_prompt = f"{sketch_base}, {user_prompt}"
    
    return full_prompt


def update_workflow(workflow, prompt, negative_prompt, resolution, steps, cfg_scale, seed, output_filename):
    """Update workflow with parameters"""
    # Find nodes by type
    for node in workflow['nodes']:
        # Update CheckpointLoaderSimple - ensure correct model name
        if node.get('type') == 'CheckpointLoaderSimple':
            node['widgets_values'] = ["dreamshaperXL_lightningDPMSDE.safetensors"]
        
        # Update positive prompt (CLIPTextEncode node 2)
        elif node.get('id') == 2 and node.get('type') == 'CLIPTextEncode':
            node['widgets_values'] = [prompt]
        
        # Update negative prompt (CLIPTextEncode node 3)
        elif node.get('id') == 3 and node.get('type') == 'CLIPTextEncode':
            node['widgets_values'] = [negative_prompt]
        
        # Update resolution (EmptyLatentImage node 4)
        elif node.get('id') == 4 and node.get('type') == 'EmptyLatentImage':
            node['widgets_values'] = [resolution[0], resolution[1], 1]
        
        # Update sampler settings (KSampler node 5)
        elif node.get('id') == 5 and node.get('type') == 'KSampler':
            node['widgets_values'] = [seed, "fixed", steps, cfg_scale, "dpmpp_2m", "karras", 1.0]
        
        # Update output filename (SaveImage node 7)
        elif node.get('id') == 7 and node.get('type') == 'SaveImage':
            node['widgets_values'] = [output_filename]
    
    return workflow


def generate_sketch_image(prompt, negative_prompt="", resolution=(768, 1344), 
                          steps=6, cfg_scale=2.0, seed=-1, output_dir="output/sketches",
                          style="sketch", output_filename=None):
    """
    Generate a sketch-based static image
    
    Args:
        prompt: Base prompt (will be enhanced with sketch keywords)
        negative_prompt: Negative prompt (default sketch negative)
        resolution: (width, height) tuple
        steps: Number of sampling steps
        cfg_scale: CFG scale
        seed: Random seed (-1 for random)
        output_dir: Output directory
        style: Style type - "sketch", "character", "object", "scene"
        output_filename: Custom output filename (without extension)
    """
    config = load_config()
    api_url = config.get('comfyui_url', 'http://127.0.0.1:8188')
    
    # Build full sketch prompt
    full_prompt = build_sketch_prompt(prompt, style)
    
    # Default negative prompt if not provided
    # Explicitly exclude color, digital art, and speech bubbles
    if not negative_prompt:
        negative_prompt = (
            "color, colors, polychrome, 3d render, photo, photorealistic, "
            "digital art, shiny, glossy, plastic, "
            "text, watermark, signature, speech bubble, dialogue box, "
            "bad anatomy, deformed, disfigured, extra limbs, "
            "blur, blurry, smooth, clean lines, vector art"
        )
    
    # Generate output filename if not provided
    if not output_filename:
        # Create safe filename from prompt
        safe_name = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        output_filename = f"sketch_{safe_name}"
    
    # Load workflow template
    workflow_path = project_root / "workflows" / "basic_image.json"
    if not workflow_path.exists():
        print(f"Error: Workflow not found at {workflow_path}")
        return None
    
    with open(workflow_path, 'r') as f:
        workflow_array = json.load(f)
    
    # Update workflow with parameters (array format)
    workflow_array = update_workflow(workflow_array, full_prompt, negative_prompt, resolution,
                              steps, cfg_scale, seed, output_filename)
    
    # Convert to API format
    from scripts.batch_generate_sketches import convert_workflow_to_api_format
    workflow = convert_workflow_to_api_format(workflow_array)
    
    print(f"Generating sketch image...")
    print(f"Prompt: {full_prompt[:80]}...")
    print(f"Resolution: {resolution[0]}x{resolution[1]}")
    print(f"Steps: {steps}, CFG: {cfg_scale}, Seed: {seed}")
    
    # Queue prompt
    try:
        result = queue_prompt(api_url, workflow)
        prompt_id = result['prompt_id']
        print(f"Queued. Prompt ID: {prompt_id}")
    except Exception as e:
        print(f"Error connecting to ComfyUI: {e}")
        print("Make sure ComfyUI is running: ./scripts/start_comfyui.sh")
        return None
    
    # Wait for completion
    print("Generating... (this may take 30-60 seconds)")
    max_wait = 300  # 5 minutes max
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        time.sleep(3)
        history = get_history(api_url, prompt_id)
        
        if prompt_id in history:
            outputs = history[prompt_id]['outputs']
            if outputs:
                print("Generation complete!")
                break
    else:
        print("Timeout waiting for generation")
        return None
    
    # Download result
    output_data = history[prompt_id]['outputs']
    for node_id, node_output in output_data.items():
        if 'images' in node_output:
            for image_info in node_output['images']:
                filename = image_info['filename']
                subfolder = image_info.get('subfolder', '')
                image_data = get_image(api_url, filename, subfolder, 'output')
                
                # Save to output directory
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, filename)
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"✓ Saved: {output_path}")
                return output_path
    
    print("No image output found")
    return None


def main():
    parser = argparse.ArgumentParser(description='Generate sketch-based static images')
    parser.add_argument('--prompt', required=True, help='Base prompt (will be enhanced with sketch keywords)')
    parser.add_argument('--negative', default='', help='Negative prompt (optional, has good default)')
    parser.add_argument('--resolution', default='768x768', help='Resolution (WxH)')
    parser.add_argument('--steps', type=int, default=6, help='Sampling steps (6 for Lightning, 25-30 for standard)')
    parser.add_argument('--cfg', type=float, default=2.0, help='CFG scale (2.0 for Lightning, 6-8 for standard)')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (-1 for random)')
    parser.add_argument('--output', default='output/sketches', help='Output directory')
    parser.add_argument('--style', default='sketch', choices=['sketch', 'character', 'object', 'scene'],
                       help='Style type')
    parser.add_argument('--filename', default=None, help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    # Parse resolution
    width, height = map(int, args.resolution.split('x'))
    
    result = generate_sketch_image(
        prompt=args.prompt,
        negative_prompt=args.negative,
        resolution=(width, height),
        steps=args.steps,
        cfg_scale=args.cfg,
        seed=args.seed,
        output_dir=args.output,
        style=args.style,
        output_filename=args.filename
    )
    
    if result:
        print(f"\n✓ Success! Image saved to: {result}")
    else:
        print("\n✗ Generation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

