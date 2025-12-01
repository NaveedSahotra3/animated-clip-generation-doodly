#!/usr/bin/env python3
"""
Generate voiceover using TTS
Supports: Coqui TTS, Piper TTS, macOS say
Usage: python scripts/generate_voiceover.py --text "Your text" --engine coqui
"""

import argparse
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def generate_coqui_tts(text, output_path, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """Generate voiceover using Coqui TTS"""
    try:
        from TTS.api import TTS
        tts = TTS(model_name=model_name)
        tts.tts_to_file(text=text, file_path=output_path)
        return True
    except ImportError:
        print("Error: Coqui TTS not installed. Run: pip install TTS")
        return False
    except Exception as e:
        print(f"Error generating with Coqui TTS: {e}")
        return False


def generate_piper_tts(text, output_path, model_path=None):
    """Generate voiceover using Piper TTS"""
    if model_path is None:
        model_path = project_root / "models" / "piper" / "en_US-lessac-medium.onnx"
    
    if not Path(model_path).exists():
        print(f"Error: Piper model not found at {model_path}")
        print("Download from: https://huggingface.co/rhasspy/piper-voices")
        return False
    
    try:
        import piper
        # Piper TTS implementation
        # This is a simplified version - actual implementation may vary
        print("Piper TTS generation not fully implemented")
        print("Please use Coqui TTS or macOS say instead")
        return False
    except Exception as e:
        print(f"Error with Piper TTS: {e}")
        return False


def generate_macos_say(text, output_path):
    """Generate voiceover using macOS built-in say command"""
    try:
        # Convert to AIFF first
        aiff_path = str(output_path).replace('.wav', '.aiff')
        subprocess.run(['say', '-o', aiff_path, text], check=True)
        
        # Convert AIFF to WAV using ffmpeg or sox
        try:
            subprocess.run(['ffmpeg', '-i', aiff_path, '-y', output_path], 
                         check=True, capture_output=True)
            Path(aiff_path).unlink()  # Remove AIFF file
            return True
        except FileNotFoundError:
            print("Warning: ffmpeg not found. Keeping AIFF format.")
            print(f"Output saved as: {aiff_path}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error with macOS say: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate voiceover')
    parser.add_argument('--text', required=True, help='Text to speak')
    parser.add_argument('--output', default='voiceover.wav', help='Output file path')
    parser.add_argument('--engine', choices=['coqui', 'piper', 'macos'], 
                       default='macos', help='TTS engine to use')
    parser.add_argument('--model', help='Model name/path (for coqui/piper)')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating voiceover: {args.text[:50]}...")
    print(f"Engine: {args.engine}")
    print(f"Output: {output_path}")
    
    success = False
    
    if args.engine == 'coqui':
        model = args.model or "tts_models/en/ljspeech/tacotron2-DDC"
        success = generate_coqui_tts(args.text, str(output_path), model)
    elif args.engine == 'piper':
        success = generate_piper_tts(args.text, str(output_path), args.model)
    elif args.engine == 'macos':
        success = generate_macos_say(args.text, str(output_path))
    
    if success:
        print(f"\n✓ Voiceover saved to: {output_path}")
    else:
        print("\n✗ Voiceover generation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

