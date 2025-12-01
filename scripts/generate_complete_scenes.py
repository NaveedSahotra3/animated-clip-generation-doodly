#!/usr/bin/env python3
"""
Generate complete scenes: images + voiceover from complete_script.json
Processes each scene sequentially: generates sketch image and voice chunks

Usage:
    python3 scripts/generate_complete_scenes.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.batch_generate_sketches import (
    generate_single_sketch, convert_workflow_to_api_format,
    queue_prompt, get_image, get_history, build_sketch_prompt, update_workflow
)
from scripts.generate_openai_voiceover import (
    split_text_into_chunks, convert_pcm_to_mp3
)
from config.generation_config import load_config
import requests
import time
import random


def load_script(file_path: Path) -> List[dict]:
    """Load complete script JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_scene_image(
    scene_num: int,
    visual_prompt: str,
    output_dir: Path,
    api_url: str,
    workflow_path: Path,
    resolution=(1024, 768),
    steps=20,
    cfg_scale=7.0
) -> Tuple[bool, Path]:
    """
    Generate sketch image for a scene
    
    Returns:
        (success, output_path)
    """
    try:
        # Build full sketch prompt
        full_prompt = build_sketch_prompt(visual_prompt, "sketch")
        negative_prompt = "colored, photo realistic, complex background, shadows, gradients, multiple subjects, blurry, low quality, detailed, realistic, watermark, text"
        
        # Output filename
        output_filename = f"scene_{scene_num}"
        
        # Load workflow
        with open(workflow_path, 'r') as f:
            workflow_array = json.load(f)
        
        # Update workflow
        seed = random.randint(0, 2**31 - 1)
        workflow_array = update_workflow(
            workflow_array, full_prompt, negative_prompt, resolution,
            steps, cfg_scale, seed, output_filename
        )
        
        # Convert to API format
        workflow = convert_workflow_to_api_format(workflow_array)
        
        print(f"   Generating image...")
        
        # Queue prompt
        result = queue_prompt(api_url, workflow)
        if 'error' in result:
            return (False, None)
        
        prompt_id = result.get('prompt_id') or result.get('number')
        if not prompt_id:
            return (False, None)
        
        # Wait for completion
        max_wait = 180
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(2)
            history = get_history(api_url, prompt_id)
            
            if prompt_id in history:
                outputs = history[prompt_id]['outputs']
                if outputs:
                    break
        else:
            return (False, None)
        
        # Download result
        output_data = history[prompt_id]['outputs']
        for node_id, node_output in output_data.items():
            if 'images' in node_output:
                for image_info in node_output['images']:
                    filename = image_info['filename']
                    subfolder = image_info.get('subfolder', '')
                    image_data = get_image(api_url, filename, subfolder, 'output')
                    
                    # Save to output directory
                    output_path = output_dir / f"scene_{scene_num}.png"
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    return (True, output_path)
        
        return (False, None)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return (False, None)


async def generate_voice_chunk(
    text: str,
    scene_num: int,
    chunk_letter: str,
    output_dir: Path,
    api_url: str,
    voice: str = "onyx",
    instructions: str = None
) -> Tuple[bool, Path]:
    """
    Generate a single voice chunk and save as MP3
    
    Returns:
        (success, output_path)
    """
    try:
        from openai import AsyncOpenAI
        
        # Initialize client for open source API
        client = AsyncOpenAI(base_url=api_url, api_key="not-needed")
        
        # Default dramatic instructions
        if instructions is None:
            instructions = """Voice Affect: Dramatic, powerful, and commanding; project authority and intensity.

Tone: Serious, intense, and compelling—express urgency and importance.

Pacing: Varied and dynamic; slower for emphasis on key points, faster for building tension.

Emotion: Strong conviction and gravitas; speak with deep resonance and bass.

Pronunciation: Clear and precise, emphasizing critical words to reinforce impact.

Pauses: Strategic pauses after important statements, creating dramatic effect."""
        
        # Generate speech
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            instructions=instructions,
            response_format="pcm"
        ) as response:
            # Save PCM chunk
            pcm_path = output_dir / f"voice_scene_{scene_num}_{chunk_letter}.pcm"
            with open(pcm_path, 'wb') as f:
                async for chunk in response.iter_bytes():
                    f.write(chunk)
        
        # Convert to MP3
        mp3_path = output_dir / f"voice_scene_{scene_num}_{chunk_letter}.mp3"
        if convert_pcm_to_mp3(pcm_path, mp3_path):
            return (True, mp3_path)
        else:
            return (False, None)
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return (False, None)


def split_voice_text(text: str, max_chars: int = 1000) -> List[Tuple[str, str]]:
    """
    Split voice text into chunks
    
    Returns:
        List of (chunk_text, chunk_letter) tuples
    """
    if len(text) <= max_chars:
        return [("A", text)]
    
    chunks = split_text_into_chunks(text, max_chars=max_chars, overlap=0)
    letters = []
    
    for i, chunk in enumerate(chunks):
        letter = chr(ord('A') + i)  # A, B, C, ...
        letters.append((letter, chunk))
    
    return letters


async def process_scene(
    scene: dict,
    output_dir: Path,
    comfyui_url: str,
    tts_url: str,
    workflow_path: Path,
    scene_index: int,
    total_scenes: int
) -> bool:
    """
    Process a single scene: generate image + voice chunks
    
    Returns:
        True if successful
    """
    scene_num = scene['scene_number']
    visual_prompt = scene['visual_prompt']
    voice_text = scene['voice_over']
    
    print(f"\n{'='*60}")
    print(f"🎬 Scene {scene_num}/{total_scenes}")
    print(f"{'='*60}")
    print(f"Visual: {visual_prompt[:60]}...")
    print(f"Voice: {len(voice_text)} characters")
    
    # Generate image
    print(f"\n📸 Generating image...")
    success, image_path = generate_scene_image(
        scene_num, visual_prompt, output_dir,
        comfyui_url, workflow_path
    )
    
    if not success:
        print(f"   ❌ Failed to generate image")
        return False
    
    print(f"   ✅ Saved: {image_path.name}")
    
    # Generate voice chunks
    voice_chunks = split_voice_text(voice_text, max_chars=1000)
    print(f"\n🎤 Generating voice ({len(voice_chunks)} chunk(s))...")
    
    all_voice_success = True
    for chunk_letter, chunk_text in voice_chunks:
        print(f"   Generating chunk {chunk_letter} ({len(chunk_text)} chars)...")
        
        success, voice_path = await generate_voice_chunk(
            chunk_text, scene_num, chunk_letter,
            output_dir, tts_url
        )
        
        if success:
            print(f"   ✅ Saved: {voice_path.name}")
        else:
            print(f"   ❌ Failed to generate chunk {chunk_letter}")
            all_voice_success = False
    
    return all_voice_success


async def main():
    """Main function"""
    # Load script
    script_path = project_root / "scripts" / "complete_script.json"
    if not script_path.exists():
        print(f"❌ Script file not found: {script_path}")
        sys.exit(1)
    
    scenes = load_script(script_path)
    if not scenes:
        print("❌ No scenes found in script")
        sys.exit(1)
    
    print(f"📝 Loaded {len(scenes)} scenes from script")
    
    # Setup output directory
    output_dir = project_root / "output" / "survival" / "script"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    
    # Load config
    config = load_config()
    comfyui_url = config.get('comfyui_url', 'http://127.0.0.1:8188')
    tts_url = os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1")
    
    # Check services
    try:
        requests.get(f"{comfyui_url}/system_stats", timeout=5)
        print(f"✅ ComfyUI: Running at {comfyui_url}")
    except:
        print(f"❌ ComfyUI not running at {comfyui_url}")
        print("   Start with: ./scripts/start_comfyui.sh")
        sys.exit(1)
    
    try:
        requests.get(f"{tts_url.replace('/v1', '')}/health", timeout=5)
        print(f"✅ TTS Server: Running at {tts_url}")
    except:
        print(f"⚠️  TTS Server may not be running at {tts_url}")
        print("   Start with: ./scripts/start_tts_server.sh")
    
    # Load workflow
    workflow_path = project_root / "workflows" / "basic_image.json"
    if not workflow_path.exists():
        print(f"❌ Workflow not found: {workflow_path}")
        sys.exit(1)
    
    print(f"\n🚀 Starting generation...")
    print(f"{'='*60}\n")
    
    # Process each scene
    successful = 0
    failed = 0
    
    for idx, scene in enumerate(scenes, 1):
        success = await process_scene(
            scene, output_dir, comfyui_url, tts_url,
            workflow_path, idx, len(scenes)
        )
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Small delay between scenes
        if idx < len(scenes):
            print(f"\n⏳ Waiting 3 seconds before next scene...\n")
            await asyncio.sleep(3)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 GENERATION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful}/{len(scenes)}")
    print(f"❌ Failed: {failed}/{len(scenes)}")
    print(f"📁 Output: {output_dir}")
    print(f"{'='*60}\n")
    
    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())

