#!/usr/bin/env python3
"""
Batch generate multiple clips from a script file
Usage: python scripts/batch_generate.py --script projects/example/script.txt
"""

import argparse
import json
import yaml
from pathlib import Path
import sys
from generate_clip import generate_clip

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def parse_script(script_path):
    """Parse script file into clip definitions"""
    clips = []
    
    with open(script_path, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse format: "Description (duration)" or "Description - duration"
        if '(' in line and ')' in line:
            desc = line[:line.rindex('(')].strip()
            duration_str = line[line.rindex('(')+1:line.rindex(')')]
            duration = float(duration_str.replace('sec', '').replace('s', '').strip())
        elif ' - ' in line:
            parts = line.split(' - ', 1)
            desc = parts[0].strip()
            duration = float(parts[1].replace('sec', '').replace('s', '').strip())
        else:
            desc = line
            duration = 2.0  # Default
        
        clips.append({
            'id': i,
            'description': desc,
            'duration': duration,
            'prompt': f"simple line drawing of {desc}, white background, clean black lines, minimalist sketch, hand drawn style"
        })
    
    return clips


def batch_generate(script_path, output_dir="projects/output/clips"):
    """Generate all clips from script"""
    clips = parse_script(script_path)
    
    print(f"Found {len(clips)} clips to generate")
    print(f"Output directory: {output_dir}")
    print()
    
    results = []
    
    for clip in clips:
        print(f"\n[{clip['id']}/{len(clips)}] {clip['description']}")
        print(f"Duration: {clip['duration']}s")
        
        output_path = generate_clip(
            prompt=clip['prompt'],
            negative_prompt="colored, realistic, complex background, shadows, multiple characters",
            duration=clip['duration'],
            output_dir=output_dir
        )
        
        if output_path:
            results.append({
                'clip': clip,
                'file': output_path
            })
            print(f"✓ Generated: {output_path}")
        else:
            print(f"✗ Failed to generate clip {clip['id']}")
    
    # Save manifest
    manifest_path = Path(output_dir) / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Batch generation complete!")
    print(f"Manifest saved to: {manifest_path}")
    print(f"Generated {len(results)}/{len(clips)} clips")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Batch generate clips from script')
    parser.add_argument('--script', required=True, help='Script file path')
    parser.add_argument('--output', default='projects/output/clips', help='Output directory')
    
    args = parser.parse_args()
    
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        sys.exit(1)
    
    batch_generate(script_path, args.output)


if __name__ == '__main__':
    main()

