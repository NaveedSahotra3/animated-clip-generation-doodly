#!/usr/bin/env python3
"""
Batch generate sketch images from a prompts file
Optimized for speed and quality for YouTube channel production

Usage: 
    python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt
    python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --parallel 3
"""

import argparse
import json
import requests
import time
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.generation_config import load_config

# Import helper functions (defined inline to avoid circular imports)
def queue_prompt(api_url, prompt_workflow):
    """Queue a prompt to ComfyUI API"""
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = requests.post(f"{api_url}/prompt", data=data)
    try:
        return req.json()
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response: {req.text[:200]}")
        raise

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
    """Build a complete sketch prompt"""
    sketch_base = "simple line drawing, white background, clean black lines, minimalist style, hand drawn sketch"
    style_additions = {
        "sketch": "",
        "character": "full body, cartoon style, friendly expression",
        "object": "front view, children's book illustration",
        "scene": "simple composition, minimalist"
    }
    addition = style_additions.get(style, "")
    if addition:
        return f"{user_prompt}, {addition}, {sketch_base}"
    return f"{user_prompt}, {sketch_base}"

def convert_workflow_to_api_format(workflow_array):
    """Convert array-based workflow to API format (object with node IDs as keys)"""
    api_workflow = {}
    
    # Build link map: link_id -> (source_node, source_slot, target_node, target_slot, type)
    link_map = {}
    for link in workflow_array['links']:
        # Link format: [link_id, source_node, source_slot, target_node, target_slot, type]
        link_id = link[0]
        source_node = link[1]
        source_slot = link[2]
        target_node = link[3]
        target_slot = link[4]
        link_map[link_id] = (source_node, source_slot, target_node, target_slot)
    
    # Convert each node
    for node in workflow_array['nodes']:
        node_id = str(node['id'])
        api_workflow[node_id] = {
            "inputs": {},
            "class_type": node.get('class_type', node['type'])
        }
        
        # Add widget values first (direct inputs)
        if 'widgets_values' in node:
            widgets = node['widgets_values']
            node_type = node.get('type', '')
            
            if node_type == 'CheckpointLoaderSimple':
                api_workflow[node_id]["inputs"]["ckpt_name"] = widgets[0]
            elif node_type == 'CLIPTextEncode':
                api_workflow[node_id]["inputs"]["text"] = widgets[0]
            elif node_type == 'EmptyLatentImage':
                api_workflow[node_id]["inputs"]["width"] = widgets[0]
                api_workflow[node_id]["inputs"]["height"] = widgets[1]
                api_workflow[node_id]["inputs"]["batch_size"] = widgets[2] if len(widgets) > 2 else 1
            elif node_type == 'KSampler':
                api_workflow[node_id]["inputs"]["seed"] = widgets[0]
                api_workflow[node_id]["inputs"]["steps"] = widgets[2]
                api_workflow[node_id]["inputs"]["cfg"] = widgets[3]
                api_workflow[node_id]["inputs"]["sampler_name"] = widgets[4]
                api_workflow[node_id]["inputs"]["scheduler"] = widgets[5]
                api_workflow[node_id]["inputs"]["denoise"] = widgets[6] if len(widgets) > 6 else 1.0
            elif node_type == 'SaveImage':
                api_workflow[node_id]["inputs"]["filename_prefix"] = widgets[0]
        
        # Add inputs from node inputs (connected inputs)
        if 'inputs' in node:
            for inp in node['inputs']:
                if 'link' in inp:
                    link_id = inp['link']
                    if link_id in link_map:
                        source_node, source_slot, _, _ = link_map[link_id]
                        api_workflow[node_id]["inputs"][inp['name']] = [str(source_node), source_slot]
    
    return api_workflow

def update_workflow(workflow, prompt, negative_prompt, resolution, steps, cfg_scale, seed, output_filename):
    """Update workflow with parameters - works with array format"""
    for node in workflow['nodes']:
        if node.get('type') == 'CheckpointLoaderSimple':
            node['widgets_values'] = ["dreamshaperXL_lightningDPMSDE.safetensors"]
        elif node.get('id') == 2 and node.get('type') == 'CLIPTextEncode':
            node['widgets_values'] = [prompt]
        elif node.get('id') == 3 and node.get('type') == 'CLIPTextEncode':
            node['widgets_values'] = [negative_prompt]
        elif node.get('id') == 4 and node.get('type') == 'EmptyLatentImage':
            node['widgets_values'] = [resolution[0], resolution[1], 1]
        elif node.get('id') == 5 and node.get('type') == 'KSampler':
            node['widgets_values'] = [seed, "fixed", steps, cfg_scale, "dpmpp_2m", "karras", 1.0]
        elif node.get('id') == 7 and node.get('type') == 'SaveImage':
            node['widgets_values'] = [output_filename]
    return workflow


def parse_prompts_file(file_path):
    """
    Parse prompts from a text file
    Format: 
        name:
        Prompt text here...
    """
    prompts = {}
    current_name = None
    current_prompt = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            original_line = line
            line = line.rstrip()  # Keep leading spaces, remove trailing
            
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Check if it's a name line (ends with colon, no leading space)
            if line.endswith(':') and not line.startswith(' '):
                # Save previous prompt
                if current_name and current_prompt:
                    prompts[current_name] = ' '.join(current_prompt).strip()
                
                # Start new prompt
                current_name = line[:-1].strip()  # Remove colon
                current_prompt = []
            else:
                # Add to current prompt (preserve line breaks for multi-line prompts)
                if current_prompt:
                    current_prompt.append(' ')
                current_prompt.append(line.strip())
    
    # Don't forget the last one
    if current_name and current_prompt:
        prompts[current_name] = ' '.join(current_prompt).strip()
    
    return prompts


def generate_single_sketch(name, prompt, api_url, workflow_path, output_dir, 
                          resolution=(1024, 768), steps=20, cfg_scale=7.0, 
                          seed=-1, style="sketch", scene_number=None):
    """Generate a single sketch image (optimized for speed)
    Returns: (name, success, output_path, error_message)
    """
    import random
    # Convert -1 (random) to actual random seed (API requires >= 0)
    if seed == -1:
        seed = random.randint(0, 2**31 - 1)
    
    try:
        # Build full sketch prompt
        full_prompt = build_sketch_prompt(prompt, style)
        negative_prompt = "colored, photo realistic, complex background, shadows, gradients, multiple subjects, blurry, low quality, detailed, realistic, watermark, text"
        
        # Generate output filename as scene-N.png (sequential number)
        if scene_number is not None:
            output_filename = f"scene-{scene_number}"
        else:
            # Fallback to name-based if no number provided
            safe_name = name.replace(' ', '_').replace('/', '_')
            output_filename = f"sketch_{safe_name}"
        
        # Load workflow
        with open(workflow_path, 'r') as f:
            workflow_array = json.load(f)
        
        # Update workflow (array format)
        workflow_array = update_workflow(workflow_array, full_prompt, negative_prompt, resolution,
                                        steps, cfg_scale, seed, output_filename)
        
        # Convert to API format
        workflow = convert_workflow_to_api_format(workflow_array)
        
        # Queue prompt
        result = queue_prompt(api_url, workflow)
        if 'error' in result:
            error_msg = result.get('error', {}).get('message', 'Unknown error')
            node_errors = result.get('node_errors', {})
            if node_errors:
                error_details = json.dumps(node_errors, indent=2)[:500]
                return (name, False, None, f"API error: {error_msg}\nDetails: {error_details}")
            return (name, False, None, f"API error: {error_msg}")
        prompt_id = result.get('prompt_id') or result.get('number')
        if not prompt_id:
            return (name, False, None, f"Unexpected API response: {result}")
        
        # Wait for completion (optimized polling)
        max_wait = 180  # 3 minutes max per image
        start_time = time.time()
        poll_interval = 2  # Check every 2 seconds
        
        while time.time() - start_time < max_wait:
            time.sleep(poll_interval)
            history = get_history(api_url, prompt_id)
            
            if prompt_id in history:
                outputs = history[prompt_id]['outputs']
                if outputs:
                    break
        else:
            return (name, False, None, "Timeout waiting for generation")
        
        # Download result
        output_data = history[prompt_id]['outputs']
        for node_id, node_output in output_data.items():
            if 'images' in node_output:
                for image_info in node_output['images']:
                    filename = image_info['filename']
                    subfolder = image_info.get('subfolder', '')
                    image_data = get_image(api_url, filename, subfolder, 'output')
                    
                    # Save to output directory with scene-N.png naming
                    os.makedirs(output_dir, exist_ok=True)
                    if scene_number is not None:
                        # Rename to scene-N.png
                        file_ext = os.path.splitext(filename)[1] or '.png'
                        final_filename = f"scene-{scene_number}{file_ext}"
                    else:
                        final_filename = filename
                    
                    output_path = os.path.join(output_dir, final_filename)
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    return (name, True, output_path, None)
        
        return (name, False, None, "No image output found")
        
    except Exception as e:
        return (name, False, None, str(e))


def batch_generate_sketches(prompts_file, output_dir="output/survival/images", 
                           resolution=(1024, 768), steps=20, cfg_scale=7.0,
                           seed=-1, style="sketch", parallel=1, delay=5):
    """
    Batch generate sketch images
    
    Args:
        prompts_file: Path to prompts text file
        output_dir: Output directory
        resolution: (width, height) tuple
        steps: Sampling steps (20 for speed, 25-30 for quality)
        cfg_scale: CFG scale (7.0 optimized)
        seed: Random seed (-1 for random)
        style: Style type
        parallel: Number of parallel generations (1 = sequential)
        delay: Delay between requests when sequential (seconds)
    """
    config = load_config()
    api_url = config.get('comfyui_url', 'http://127.0.0.1:8188')
    
    # Check if ComfyUI is running
    try:
        requests.get(f"{api_url}/system_stats", timeout=5)
    except:
        print("❌ Error: ComfyUI is not running!")
        print("Start it with: ./scripts/start_comfyui.sh")
        return []
    
    # Load prompts
    prompts = parse_prompts_file(prompts_file)
    if not prompts:
        print(f"❌ No prompts found in {prompts_file}")
        return []
    
    print(f"📝 Loaded {len(prompts)} prompts from {prompts_file}")
    print(f"⚙️  Settings: {resolution[0]}x{resolution[1]}, {steps} steps, CFG {cfg_scale}")
    print(f"🚀 Mode: {'Parallel' if parallel > 1 else 'Sequential'}")
    print("-" * 60)
    
    # Load workflow template
    workflow_path = project_root / "workflows" / "basic_image.json"
    if not workflow_path.exists():
        print(f"❌ Workflow not found at {workflow_path}")
        return []
    
    results = []
    start_time = time.time()
    
    if parallel > 1:
        # Parallel generation
        print(f"🔄 Generating {len(prompts)} images in parallel (max {parallel} at once)...\n")
        
        # Create list of (index, name, prompt) tuples to preserve order
        prompts_list = list(prompts.items())
        
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(
                    generate_single_sketch,
                    name, prompt, api_url, workflow_path, output_dir,
                    resolution, steps, cfg_scale, seed, style, idx + 1
                ): (idx, name)
                for idx, (name, prompt) in enumerate(prompts_list)
            }
            
            completed = 0
            for future in as_completed(futures):
                idx, name = futures[future]
                completed += 1
                try:
                    result = future.result()
                    results.append(result)
                    result_name, success, path, error = result
                    
                    if success:
                        print(f"✅ [{completed}/{len(prompts)}] Scene {idx + 1}: {name}")
                        print(f"   Saved: {path}")
                    else:
                        print(f"❌ [{completed}/{len(prompts)}] Scene {idx + 1}: {name}")
                        print(f"   Error: {error}")
                except Exception as e:
                    print(f"❌ [{completed}/{len(prompts)}] Scene {idx + 1}: {name}")
                    print(f"   Exception: {e}")
                    results.append((name, False, None, str(e)))
                
                print()
    else:
        # Sequential generation
        print(f"🔄 Generating {len(prompts)} images sequentially...\n")
        
        for idx, (name, prompt) in enumerate(prompts.items(), 1):
            print(f"[{idx}/{len(prompts)}] Generating Scene {idx}: {name}...")
            
            result = generate_single_sketch(
                name, prompt, api_url, workflow_path, output_dir,
                resolution, steps, cfg_scale, seed, style, scene_number=idx
            )
            results.append(result)
            
            result_name, success, path, error = result
            if success:
                print(f"✅ Success! Saved: {path}")
            else:
                print(f"❌ Failed: {error}")
            
            # Delay between requests (except for last one)
            if idx < len(prompts) and delay > 0:
                print(f"⏳ Waiting {delay}s before next generation...\n")
                time.sleep(delay)
            else:
                print()
    
    # Summary
    elapsed = time.time() - start_time
    successful = sum(1 for r in results if r[1])
    failed = len(results) - successful
    
    print("=" * 60)
    print("📊 BATCH GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    if successful > 0:
        print(f"⚡ Average time per image: {elapsed/successful:.1f} seconds")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 60)
    
    if failed > 0:
        print("\n❌ Failed prompts:")
        for name, success, path, error in results:
            if not success:
                print(f"   - {name}: {error}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Batch generate sketch images for YouTube channel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all prompts sequentially
  python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt
  
  # Generate 3 at a time in parallel (faster)
  python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --parallel 3
  
  # High quality, slower
  python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --steps 30 --resolution 1024x1024
  
  # Fast mode (lower quality, faster)
  python scripts/batch_generate_sketches.py --file templates/youtube_sketch_prompts.txt --steps 15 --parallel 2
        """
    )
    parser.add_argument('--file', required=True, help='Prompts file path')
    parser.add_argument('--output', default='output/survival/images', help='Output directory')
    parser.add_argument('--resolution', default='1024x768', help='Resolution (WxH)')
    parser.add_argument('--steps', type=int, default=20, help='Sampling steps (15=fast, 20=balanced, 30=quality)')
    parser.add_argument('--cfg', type=float, default=7.0, help='CFG scale')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (-1 for random)')
    parser.add_argument('--style', default='sketch', choices=['sketch', 'character', 'object', 'scene'],
                       help='Style type')
    parser.add_argument('--parallel', type=int, default=1, 
                       help='Number of parallel generations (1=sequential, 2-3 recommended)')
    parser.add_argument('--delay', type=int, default=5, 
                       help='Delay between requests when sequential (seconds)')
    
    args = parser.parse_args()
    
    # Parse resolution
    width, height = map(int, args.resolution.split('x'))
    
    # Validate prompts file
    prompts_path = Path(args.file)
    if not prompts_path.is_absolute():
        prompts_path = project_root / prompts_path
    
    if not prompts_path.exists():
        print(f"❌ Prompts file not found: {prompts_path}")
        sys.exit(1)
    
    results = batch_generate_sketches(
        prompts_path,
        output_dir=args.output,
        resolution=(width, height),
        steps=args.steps,
        cfg_scale=args.cfg,
        seed=args.seed,
        style=args.style,
        parallel=args.parallel,
        delay=args.delay
    )
    
    if not results:
        sys.exit(1)
    
    successful = sum(1 for r in results if r[1])
    if successful == 0:
        print("\n❌ All generations failed!")
        sys.exit(1)
    elif successful < len(results):
        print(f"\n⚠️  {len(results) - successful} generations failed")
        sys.exit(1)
    else:
        print("\n🎉 All images generated successfully!")


if __name__ == '__main__':
    main()

