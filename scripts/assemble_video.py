#!/usr/bin/env python3
"""
Assemble clips and voiceover into final video
Usage: python scripts/assemble_video.py --clips clips/ --voiceover voice.wav --output final.mp4
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def assemble_with_ffmpeg(clips_dir, voiceover_path, output_path, resolution=(1920, 1080), fps=24):
    """Assemble video using ffmpeg"""
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: ffmpeg not found. Please install: brew install ffmpeg")
        return False
    
    clips_dir = Path(clips_dir)
    
    # Find all video files
    video_files = sorted(clips_dir.glob('*.mp4')) + sorted(clips_dir.glob('*.mov'))
    
    if not video_files:
        print(f"Error: No video files found in {clips_dir}")
        return False
    
    # Create file list for concat
    concat_file = clips_dir / 'concat_list.txt'
    with open(concat_file, 'w') as f:
        for video in video_files:
            f.write(f"file '{video.absolute()}'\n")
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
    ]
    
    # Add voiceover if provided
    if voiceover_path and Path(voiceover_path).exists():
        cmd.extend([
            '-i', str(Path(voiceover_path).absolute()),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
        ])
    else:
        cmd.extend([
            '-c:v', 'libx264',
        ])
    
    # Output settings
    cmd.extend([
        '-pix_fmt', 'yuv420p',
        '-r', str(fps),
        '-y',  # Overwrite output
        str(Path(output_path).absolute())
    ])
    
    print("Assembling video...")
    print(f"Clips: {len(video_files)}")
    print(f"Output: {output_path}")
    
    try:
        subprocess.run(cmd, check=True)
        concat_file.unlink()  # Clean up
        print(f"\n✓ Video assembled: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error assembling video: {e}")
        return False


def assemble_from_manifest(manifest_path, voiceover_path, output_path):
    """Assemble video from manifest JSON"""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    clips = [item['file'] for item in manifest if Path(item['file']).exists()]
    
    if not clips:
        print("Error: No valid clips found in manifest")
        return False
    
    # Create temporary directory with clips
    temp_dir = Path(output_path).parent / 'temp_clips'
    temp_dir.mkdir(exist_ok=True)
    
    # Copy/link clips in order
    for i, clip_path in enumerate(clips):
        ext = Path(clip_path).suffix
        link_path = temp_dir / f"clip_{i:03d}{ext}"
        if link_path.exists():
            link_path.unlink()
        link_path.symlink_to(Path(clip_path).absolute())
    
    return assemble_with_ffmpeg(temp_dir, voiceover_path, output_path)


def main():
    parser = argparse.ArgumentParser(description='Assemble clips into final video')
    parser.add_argument('--clips', help='Directory containing clips')
    parser.add_argument('--manifest', help='Manifest JSON file')
    parser.add_argument('--voiceover', help='Voiceover audio file')
    parser.add_argument('--output', required=True, help='Output video file')
    parser.add_argument('--resolution', default='1920x1080', help='Output resolution')
    parser.add_argument('--fps', type=int, default=24, help='Frame rate')
    
    args = parser.parse_args()
    
    if not args.clips and not args.manifest:
        print("Error: Must provide --clips or --manifest")
        sys.exit(1)
    
    # Parse resolution
    width, height = map(int, args.resolution.split('x'))
    
    if args.manifest:
        success = assemble_from_manifest(args.manifest, args.voiceover, args.output)
    else:
        success = assemble_with_ffmpeg(args.clips, args.voiceover, args.output, 
                                      (width, height), args.fps)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()

