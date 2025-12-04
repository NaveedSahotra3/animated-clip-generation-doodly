#!/usr/bin/env python3
"""
LLM-powered creative prompt enhancement for visual generation
Uses DeepSeek API to transform voice-over text into creative visual prompts

Usage:
    from scripts.enhance_prompt_with_llm import generate_creative_visual_prompt
    prompt = generate_creative_visual_prompt(voice_text, base_prompt="...")
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.generation_config import load_config


def generate_creative_visual_prompt(
    voice_over_text: str,
    base_prompt: Optional[str] = None,
    style: str = "graphite pencil sketch",
    creativity_level: float = 0.7
) -> str:
    """
    Generate creative visual prompt from voice-over text using DeepSeek API
    
    Args:
        voice_over_text: The narration/script text
        base_prompt: Optional existing prompt to enhance
        style: Art style description
        creativity_level: 0.0-1.0 (how creative vs literal)
    
    Returns:
        Enhanced creative prompt
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: pip install openai")
        return base_prompt or ""
    
    config = load_config()
    llm_config = config.get('llm', {})
    
    # Get API key from config or environment
    api_key = llm_config.get('api_key') or os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("Warning: DEEPSEEK_API_KEY not set. Using base prompt as-is.")
        return base_prompt or ""
    
    # Get API settings
    base_url = llm_config.get('base_url', 'https://api.deepseek.com')
    model = llm_config.get('model', 'deepseek-chat')
    temperature = llm_config.get('temperature', 0.8)
    max_tokens = llm_config.get('max_tokens', 500)
    
    # Adjust temperature based on creativity level
    effective_temp = temperature * (0.5 + creativity_level * 0.5)
    
    # Build system prompt
    system_prompt = """You are a creative visual director and professional illustrator. 
Your task is to generate detailed, visually compelling prompts for graphite pencil 
sketch illustrations that will accompany narration.

CRITICAL REQUIREMENTS:
- Style: Graphite pencil, charcoal, cross-hatching, greyscale, monochrome
- NO TEXT OVERLAYS: Never include text, words, or labels as overlays on the image
- NO TEXT ON IMAGE: Do not write text directly on the illustration
- Structured Layouts: When showing progression or stages, create clear visual sections/panels
- Panel Labels: If labels are needed (like "STAGE 1", "STAGE 2"), describe them as part of the composition structure, NOT as text overlays
- Three-Panel Layout: For multi-stage concepts, create three distinct vertical or horizontal sections/panels with clear visual divisions
- Each Panel: Should have its own character/figure with distinct visual characteristics
- Label Placement: Describe labels as "below the character" or "at the bottom of each panel" but emphasize they are part of the visual design, not text overlays

Visual Requirements:
- Include: Composition details, lighting, emotions, facial expressions, background elements
- Be creative: Use visual metaphors, interesting camera angles, dramatic moments
- Keep it: Realistic, mature, professional artistic style
- Format: Three-panel comic strip layout (triptych) when showing progression or stages
- Clear Sections: Each section/panel should be visually distinct and serve a clear purpose

AVOID:
- Text overlays, text on image, written words, labels as text
- Speech bubbles, dialogue boxes
- Color, cartoonish style
- Unclear or merged sections

Generate detailed visual prompts (150-250 words) that create structured, visually compelling 
illustrations with clear sections/panels when needed, but WITHOUT any text overlays."""

    # Build user prompt
    user_prompt = f"""Generate a detailed visual prompt for a {style} illustration 
that will accompany this narration:

"{voice_over_text}"

"""
    
    if base_prompt:
        user_prompt += f"""Base visual concept: {base_prompt}

Enhance and expand this concept with creative details, composition, lighting, 
and emotional depth. """
    else:
        user_prompt += """Create a compelling visual concept that captures the 
essence of this narration. """
    
    user_prompt += """Focus on:
- Visual storytelling and composition
- Clear section/panel divisions when showing progression or stages
- Each section should have distinct visual purpose and character
- Character emotions and expressions
- Background details that enhance the mood
- Lighting and atmosphere
- Professional artistic quality
- NO text overlays or text on the image

IMPORTANT: If the base prompt mentions stages or progression, create a three-panel layout with:
- Three distinct vertical sections/panels
- Each panel showing a different stage/character
- Clear visual divisions between panels
- Labels described as part of composition structure (below characters, at bottom of panels), NOT as text overlays

Generate the visual prompt now:"""

    # Initialize client
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        # Call API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=effective_temp,
            max_tokens=max_tokens
        )
        
        generated_prompt = response.choices[0].message.content.strip()
        
        # Clean up the prompt (remove quotes if wrapped)
        if generated_prompt.startswith('"') and generated_prompt.endswith('"'):
            generated_prompt = generated_prompt[1:-1]
        
        return generated_prompt
        
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        print("Falling back to base prompt")
        return base_prompt or ""


def test_llm_connection() -> bool:
    """Test if LLM API is configured and working"""
    try:
        from openai import OpenAI
    except ImportError:
        return False
    
    config = load_config()
    llm_config = config.get('llm', {})
    api_key = llm_config.get('api_key') or os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        return False
    
    base_url = llm_config.get('base_url', 'https://api.deepseek.com')
    model = llm_config.get('model', 'deepseek-chat')
    
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        return True
    except:
        return False


if __name__ == '__main__':
    # Test function
    test_text = "The fourth stressor: hunger and thirst. Without food and water, you weaken gradually, then suddenly."
    
    print("Testing DeepSeek LLM integration...")
    print(f"API configured: {test_llm_connection()}")
    print("\nGenerating creative prompt...")
    
    prompt = generate_creative_visual_prompt(test_text)
    print(f"\nGenerated prompt:\n{prompt}")

