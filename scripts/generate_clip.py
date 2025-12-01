#!/usr/bin/env python3
"""
Generate a single animated clip using ComfyUI API
Usage: python scripts/generate_clip.py --prompt "your prompt" --duration 2
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
    """Download generated image/video from ComfyUI"""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url = f"{api_url}/view"
    response = requests.get(url, params=data)
    return response.content


def get_history(api_url, prompt_id):
    """Get generation history"""
    response = requests.get(f"{api_url}/history/{prompt_id}")
    return response.json()


def generate_clip(prompt, negative_prompt="", duration=2, resolution=(768, 768), 
                  steps=25, cfg_scale=7.5, seed=-1, output_dir="output"):
    """
    Generate an animated clip
    
    Args:
        prompt: Positive prompt
        negative_prompt: Negative prompt
        duration: Duration in seconds (will be converted to frames at 24fps)
        resolution: (width, height) tuple
        steps: Number of sampling steps
        cfg_scale: CFG scale
        seed: Random seed (-1 for random)
        output_dir: Output directory
    """
    config = load_config()
    api_url = config.get('comfyui_url', 'http://127.0.0.1:8188')
    
    # Calculate frames (24fps)
    frame_count = int(duration * 24)
    
    # Load workflow template
    workflow_path = project_root / "workflows" / "whiteboard_animation.json"
    if not workflow_path.exists():
        print(f"Error: Workflow not found at {workflow_path}")
        print("Using basic workflow...")
        workflow = create_basic_workflow(prompt, negative_prompt, frame_count, 
                                        resolution, steps, cfg_scale, seed)
    else:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        # Update workflow with parameters
        workflow = update_workflow(workflow, prompt, negative_prompt, frame_count,
                                 resolution, steps, cfg_scale, seed)
    
    print(f"Generating clip: {prompt[:50]}...")
    print(f"Duration: {duration}s ({frame_count} frames)")
    print(f"Resolution: {resolution[0]}x{resolution[1]}")
    
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
    print("Generating... (this may take 1-5 minutes)")
    max_wait = 600  # 10 minutes max
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        time.sleep(5)
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
        if 'videos' in node_output:
            for video_info in node_output['videos']:
                filename = video_info['filename']
                subfolder = video_info.get('subfolder', '')
                video_data = get_image(api_url, filename, subfolder, 'output')
                
                # Save to output directory
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, filename)
                with open(output_path, 'wb') as f:
                    f.write(video_data)
                print(f"Saved: {output_path}")
                return output_path
    
    print("No video output found")
    return None


def create_basic_workflow(prompt, negative_prompt, frame_count, resolution, steps, cfg_scale, seed):
    """Create a basic AnimateDiff workflow"""
    # This is a simplified workflow structure
    # In practice, you'd load from the JSON template
    return {
        "1": {
            "inputs": {
                "ckpt_name": "model.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        # Add more nodes as needed
    }


def update_workflow(workflow, prompt, negative_prompt, frame_count, resolution, steps, cfg_scale, seed):
    """Update workflow with parameters"""
    # This would update the workflow JSON with actual values
    # Implementation depends on workflow structure
    return workflow


def main():
    parser = argparse.ArgumentParser(description='Generate animated clip')
    parser.add_argument('--prompt', required=True, help='Positive prompt')
    parser.add_argument('--negative', default='', help='Negative prompt')
    parser.add_argument('--duration', type=float, default=2.0, help='Duration in seconds')
    parser.add_argument('--resolution', default='768x768', help='Resolution (WxH)')
    parser.add_argument('--steps', type=int, default=25, help='Sampling steps')
    parser.add_argument('--cfg', type=float, default=7.5, help='CFG scale')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (-1 for random)')
    parser.add_argument('--output', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    # Parse resolution
    width, height = map(int, args.resolution.split('x'))
    
    result = generate_clip(
        prompt=args.prompt,
        negative_prompt=args.negative,
        duration=args.duration,
        resolution=(width, height),
        steps=args.steps,
        cfg_scale=args.cfg,
        seed=args.seed,
        output_dir=args.output
    )
    
    if result:
        print(f"\n✓ Success! Clip saved to: {result}")
    else:
        print("\n✗ Generation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

