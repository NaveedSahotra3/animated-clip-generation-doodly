#!/usr/bin/env python3
"""
Generate voiceover using OpenAI TTS API
- Handles text chunking for character limits
- Uses Onyx voice with dramatic vibe
- Converts to MP3 format
- Supports both official API and open source alternatives

Usage:
    python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt
    python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt --api openai --chunk-size 1000
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def split_text_into_chunks(text: str, max_chars: int = 1000, overlap: int = 50) -> List[str]:
    """
    Split text into chunks that respect sentence boundaries when possible
    
    Args:
        text: Full text to split
        max_chars: Maximum characters per chunk
        overlap: Characters to overlap between chunks for smooth transitions
    
    Returns:
        List of text chunks
    """
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    current_pos = 0
    text_length = len(text)
    
    while current_pos < text_length:
        # Calculate end position
        end_pos = min(current_pos + max_chars, text_length)
        
        # If not at the end, try to break at a sentence boundary
        if end_pos < text_length:
            # Look for sentence endings within the last 200 chars
            search_start = max(current_pos, end_pos - 200)
            sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']
            
            best_break = end_pos
            for ending in sentence_endings:
                # Find last occurrence of sentence ending
                last_break = text.rfind(ending, search_start, end_pos)
                if last_break != -1:
                    best_break = last_break + len(ending)
                    break
            
            end_pos = best_break
        
        # Extract chunk
        chunk = text[current_pos:end_pos].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move position (with overlap for smooth transitions)
        current_pos = end_pos - overlap if end_pos < text_length else end_pos
    
    return chunks


async def generate_chunk_openai_async(
    text: str,
    chunk_num: int,
    total_chunks: int,
    output_dir: Path,
    api_key: Optional[str] = None,
    use_open_source: bool = False,
    base_url: Optional[str] = None,
    voice: str = "onyx",
    instructions: str = "Voice Affect: Dramatic, powerful, and commanding; project authority and intensity.\n\nTone: Serious, intense, and compelling—express urgency and importance.\n\nPacing: Varied and dynamic; slower for emphasis on key points, faster for building tension.\n\nEmotion: Strong conviction and gravitas; speak with deep resonance and bass.\n\nPronunciation: Clear and precise, emphasizing critical words to reinforce impact.\n\nPauses: Strategic pauses after important statements, creating dramatic effect and allowing key points to resonate."
) -> Optional[Path]:
    """
    Generate a single chunk using OpenAI TTS (async)
    
    Returns:
        Path to generated audio file (WAV/PCM format)
    """
    try:
        from openai import AsyncOpenAI
        
        # Initialize client
        if use_open_source:
            # For open source API, no API key needed
            # Use provided base_url, or env var, or default
            api_base_url = base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1")
            client = AsyncOpenAI(base_url=api_base_url, api_key="not-needed")
            print(f"   Using open source API at: {api_base_url}")
        else:
            # Official OpenAI API requires API key
            client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        if not use_open_source and not api_key and not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OpenAI API key not found!")
            print("   Set OPENAI_API_KEY environment variable or use --api-key")
            print("   Or use --open-source flag for open source API")
            return None
        
        print(f"   Generating chunk {chunk_num}/{total_chunks} ({len(text)} chars)...")
        
        # Save chunk
        chunk_filename = output_dir / f"chunk_{chunk_num:03d}.pcm"
        
        if use_open_source:
            # Open source API uses streaming response
            async with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
                instructions=instructions,
                response_format="pcm"
            ) as response:
                with open(chunk_filename, 'wb') as f:
                    async for chunk in response.iter_bytes():
                        f.write(chunk)
        else:
            # Official OpenAI API
            response = await client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                instructions=instructions,
                response_format="pcm"
            )
            # Save the response content
            with open(chunk_filename, 'wb') as f:
                async for chunk in response.iter_bytes():
                    f.write(chunk)
        
        return chunk_filename
        
    except ImportError:
        print("❌ Error: openai library not installed")
        print("   Install with: pip install openai")
        return None
    except Exception as e:
        print(f"❌ Error generating chunk {chunk_num}: {e}")
        return None


def convert_pcm_to_mp3(pcm_file: Path, mp3_file: Path, sample_rate: int = 24000) -> bool:
    """
    Convert PCM audio file to MP3 using ffmpeg
    
    Args:
        pcm_file: Input PCM file path
        mp3_file: Output MP3 file path
        sample_rate: Sample rate of PCM file (default 24000 for OpenAI TTS)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import subprocess
        
        # Convert PCM to MP3 using ffmpeg
        # OpenAI TTS PCM format: 24kHz, 16-bit, mono
        cmd = [
            'ffmpeg',
            '-f', 's16le',  # 16-bit little-endian signed integer
            '-ar', str(sample_rate),  # Sample rate
            '-ac', '1',  # Mono
            '-i', str(pcm_file),
            '-codec:a', 'libmp3lame',
            '-b:a', '192k',  # Bitrate
            '-y',  # Overwrite
            str(mp3_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Remove PCM file after successful conversion
            pcm_file.unlink()
            return True
        else:
            print(f"⚠️  FFmpeg error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: ffmpeg not found!")
        print("   Install with: brew install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Error converting to MP3: {e}")
        return False


def merge_audio_files(audio_files: List[Path], output_file: Path) -> bool:
    """
    Merge multiple audio files into one using ffmpeg
    
    Args:
        audio_files: List of audio file paths to merge
        output_file: Output file path
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import subprocess
        
        # Create file list for ffmpeg concat
        file_list_path = output_file.parent / "concat_list.txt"
        with open(file_list_path, 'w') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file.absolute()}'\n")
        
        # Merge using ffmpeg concat
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(file_list_path),
            '-codec:a', 'libmp3lame',
            '-b:a', '192k',
            '-y',
            str(output_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # Clean up
        file_list_path.unlink()
        
        if result.returncode == 0:
            # Remove individual chunk files
            for audio_file in audio_files:
                audio_file.unlink()
            return True
        else:
            print(f"⚠️  FFmpeg merge error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: ffmpeg not found!")
        print("   Install with: brew install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Error merging audio: {e}")
        return False


async def generate_voiceover_async(
    text: str,
    output_path: Path,
    api_key: Optional[str] = None,
    use_open_source: bool = False,
    base_url: Optional[str] = None,
    chunk_size: int = 1000,
    voice: str = "onyx",
    instructions: Optional[str] = None
) -> bool:
    """
    Generate complete voiceover from text (async)
    
    Args:
        text: Full text to convert to speech
        output_path: Output MP3 file path
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        use_open_source: Use open source API alternative
        chunk_size: Maximum characters per chunk
        voice: Voice to use (onyx, alloy, echo, fable, nova, shimmer)
        instructions: Custom voice instructions
    
    Returns:
        True if successful, False otherwise
    """
    # Default dramatic instructions for Onyx voice
    if instructions is None:
        instructions = """Voice Affect: Dramatic, powerful, and commanding; project authority and intensity.

Tone: Serious, intense, and compelling—express urgency and importance.

Pacing: Varied and dynamic; slower for emphasis on key points, faster for building tension.

Emotion: Strong conviction and gravitas; speak with deep resonance and bass.

Pronunciation: Clear and precise, emphasizing critical words to reinforce impact.

Pauses: Strategic pauses after important statements, creating dramatic effect and allowing key points to resonate."""
    
    # Split text into chunks
    chunks = split_text_into_chunks(text, max_chars=chunk_size)
    total_chunks = len(chunks)
    
    print(f"📝 Text length: {len(text)} characters")
    print(f"📦 Split into {total_chunks} chunk(s)")
    print(f"🎤 Voice: {voice} (dramatic)")
    print(f"📁 Output: {output_path}")
    print("-" * 60)
    
    if total_chunks == 0:
        print("❌ No text to process")
        return False
    
    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = output_path.parent / "temp_voiceover"
    temp_dir.mkdir(exist_ok=True)
    
    # Generate all chunks
    chunk_files = []
    for i, chunk in enumerate(chunks, 1):
        chunk_file = await generate_chunk_openai_async(
            chunk,
            i,
            total_chunks,
            temp_dir,
            api_key=api_key,
            use_open_source=use_open_source,
            base_url=base_url,
            voice=voice,
            instructions=instructions
        )
        
        if chunk_file is None:
            print(f"❌ Failed to generate chunk {i}")
            # Clean up
            for f in chunk_files:
                if f.exists():
                    f.unlink()
            return False
        
        # Convert to MP3
        mp3_chunk = temp_dir / f"chunk_{i:03d}.mp3"
        if convert_pcm_to_mp3(chunk_file, mp3_chunk):
            chunk_files.append(mp3_chunk)
        else:
            print(f"⚠️  Warning: Could not convert chunk {i} to MP3, keeping PCM")
            chunk_files.append(chunk_file)
    
    # Merge all chunks
    if len(chunk_files) == 1:
        # Single chunk - just rename
        chunk_files[0].rename(output_path)
    else:
        # Multiple chunks - merge them
        print(f"\n🔗 Merging {len(chunk_files)} chunks...")
        if merge_audio_files(chunk_files, output_path):
            print(f"✅ Merged successfully!")
        else:
            print(f"❌ Failed to merge chunks")
            return False
    
    # Clean up temp directory
    try:
        temp_dir.rmdir()
    except:
        pass
    
    print(f"\n✅ Voiceover complete!")
    print(f"   Saved to: {output_path}")
    print(f"   Format: MP3")
    print(f"   Duration: ~{len(text) / 150:.1f} seconds (estimated)")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate voiceover using OpenAI TTS with Onyx voice (dramatic)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from file (uses OPENAI_API_KEY env var)
  python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt
  
  # With custom API key and chunk size
  python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt --api-key YOUR_KEY --chunk-size 800
  
  # Use open source API (if available)
  python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt --open-source
  
  # Custom output location
  python scripts/generate_openai_voiceover.py --file templates/youtube_ai_voice_generation.txt --output output/survival/voiceover.mp3
        """
    )
    parser.add_argument('--file', required=True, help='Text file to convert to speech')
    parser.add_argument('--output', default='output/survival/voiceover.mp3', help='Output MP3 file path')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('--open-source', action='store_true', help='Use open source API alternative (no API key needed)')
    parser.add_argument('--base-url', help='Custom base URL for open source API (default: http://localhost:8000/v1)')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Maximum characters per chunk')
    parser.add_argument('--voice', default='onyx', choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'],
                       help='Voice to use (default: onyx)')
    parser.add_argument('--instructions', help='Custom voice instructions (optional)')
    
    args = parser.parse_args()
    
    # Read text file
    text_file = Path(args.file)
    if not text_file.is_absolute():
        text_file = project_root / text_file
    
    if not text_file.exists():
        print(f"❌ File not found: {text_file}")
        sys.exit(1)
    
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        print(f"❌ File is empty: {text_file}")
        sys.exit(1)
    
    # Set output path
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = project_root / output_path
    
    # Run async generation
    success = asyncio.run(generate_voiceover_async(
        text=text,
        output_path=output_path,
        api_key=args.api_key,
        use_open_source=args.open_source,
        base_url=args.base_url,
        chunk_size=args.chunk_size,
        voice=args.voice,
        instructions=args.instructions
    ))
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()

