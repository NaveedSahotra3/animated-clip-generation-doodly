# 🧠 LLM Integration Plan for Creative Prompt Generation

## Current State
- **Manual prompts**: User writes `visual_prompt` in `complete_script.json`
- **Direct usage**: Prompts used as-is → ComfyUI → Image
- **Issue**: Prompts are descriptive but lack creativity, visual storytelling, artistic direction

## Goal
Add LLM layer to generate **creative, visually compelling prompts** that:
- Transform voice-over text into rich visual concepts
- Add artistic direction (composition, lighting, perspective)
- Include visual metaphors and storytelling elements
- Enhance existing prompts with creative details

---

## Architecture Options

### Option 1: DeepSeek API (FREE - Recommended)
**Pros:**
- ✅ **FREE tier available**
- Very affordable: $0.55/$2.19 per million tokens
- High quality, creative output
- Easy to implement
- Fast

**Cons:**
- Requires API key (free to get)
- External dependency

### Option 1b: Grok API (xAI)
**Pros:**
- ✅ **$25 free credits/month** (as of 2024)
- Good quality
- Fast

**Cons:**
- May require X/Twitter account
- Free tier may have limits

### Option 1c: OpenAI API
**Pros:**
- Easy to implement
- High quality (GPT-4, Claude)
- Fast
- Good creative output

**Cons:**
- Requires API key
- Costs per request (~$0.01-0.03 per prompt)
- External dependency

**Implementation:**
```python
# scripts/enhance_prompt_with_llm.py
def generate_creative_prompt(voice_text, base_prompt=None):
    """Use OpenAI to generate creative visual prompt"""
    # Uses existing openai package
```

### Option 2: Local LLM (Ollama/LM Studio)
**Pros:**
- No API costs
- Privacy (data stays local)
- Works offline
- Good for batch processing

**Cons:**
- Requires model download (3-7GB)
- Slower than API
- May need GPU for quality
- Setup complexity

**Models:**
- `llama3.1:8b` (fast, good quality)
- `mistral:7b` (creative, fast)
- `qwen2.5:7b` (good for structured output)

### Option 3: Hybrid (Best of Both)
- Use OpenAI for production/quality
- Use local LLM for development/testing
- Fallback chain: OpenAI → Local → Manual

---

## Proposed Implementation

### Phase 1: Basic LLM Prompt Enhancement

**New File:** `scripts/enhance_prompt_with_llm.py`

**Function:**
```python
def generate_creative_visual_prompt(
    voice_over_text: str,
    base_prompt: str = None,
    style: str = "graphite sketch",
    creativity_level: float = 0.7
) -> str:
    """
    Generate creative visual prompt from voice-over text
    
    Args:
        voice_over_text: The narration/script text
        base_prompt: Optional existing prompt to enhance
        style: Art style (graphite sketch, comic strip, etc.)
        creativity_level: 0.0-1.0 (how creative vs literal)
    
    Returns:
        Enhanced creative prompt
    """
```

**Prompt Template:**
```
You are a creative visual director. Generate a detailed visual prompt for a 
graphite pencil sketch illustration that will accompany this narration:

"{voice_over_text}"

Requirements:
- Style: {style} (graphite pencil, charcoal, cross-hatching, greyscale)
- Format: Three-panel comic strip layout (if applicable)
- Include: Composition, lighting, emotions, background details
- Be creative: Use visual metaphors, interesting angles, dramatic moments
- Keep it: Realistic, mature, professional artistic style

Generate a detailed visual prompt (150-250 words) that captures the essence 
and emotion of the narration while being visually compelling.
```

### Phase 2: Integration Points

**1. Update `complete_script.json` structure:**
```json
{
  "scene_number": 1,
  "voice_over": "...",
  "visual_prompt": "...",  // Optional: base prompt
  "use_llm": true,          // Flag to enable LLM enhancement
  "creativity": 0.7         // 0.0 = literal, 1.0 = very creative
}
```

**2. Update `generate_complete_scenes.py`:**
```python
# Before generating image:
if scene.get('use_llm', False):
    visual_prompt = generate_creative_visual_prompt(
        voice_text=scene['voice_over'],
        base_prompt=scene.get('visual_prompt'),
        creativity_level=scene.get('creativity', 0.7)
    )
else:
    visual_prompt = scene['visual_prompt']
```

**3. Add configuration:**
```yaml
# config/generation_config.yaml
llm:
  provider: "deepseek"  # Options: "deepseek", "grok", "openai", "ollama"
  model: "deepseek-chat"  # or "grok-beta", "gpt-4o-mini"
  api_key: null  # Set via env: DEEPSEEK_API_KEY or GROK_API_KEY
  base_url: "https://api.deepseek.com"  # or "https://api.x.ai" for Grok
  temperature: 0.8  # Creativity (0.0-1.0)
  max_tokens: 500
```

---

## Workflow Comparison

### Current Flow:
```
User writes prompt → ComfyUI → Image
```

### With LLM:
```
Voice-over text → LLM → Creative prompt → ComfyUI → Image
                    ↑
              (Optional: base prompt)
```

---

## Implementation Steps

### Step 1: Add LLM Module (OpenAI)
- [ ] Create `scripts/enhance_prompt_with_llm.py`
- [ ] Add prompt templates
- [ ] Add OpenAI integration
- [ ] Test with sample voice-over

### Step 2: Update Configuration
- [ ] Add LLM config to `generation_config.yaml`
- [ ] Add environment variable support
- [ ] Add fallback to manual prompts

### Step 3: Integrate with Generation Script
- [ ] Update `generate_complete_scenes.py`
- [ ] Add `use_llm` flag support
- [ ] Add prompt caching (optional)

### Step 4: Add Local LLM Support (Optional)
- [ ] Add Ollama client
- [ ] Add local model support
- [ ] Add fallback chain

### Step 5: Testing & Refinement
- [ ] Test with various voice-over texts
- [ ] Adjust prompt templates
- [ ] Fine-tune creativity levels

---

## Example Output

### Input (Voice-over):
```
"The fourth stressor: hunger and thirst. Without food and water, 
you weaken gradually, then suddenly..."
```

### Current Prompt:
```
"Sketch of a person growing weaker across three stages..."
```

### LLM-Enhanced Prompt:
```
"Three-panel vertical triptych in graphite pencil and charcoal. 
Panel 1: A soldier stands resolute, uniform crisp, rifle slung 
casually over shoulder, canteen in hand—the illusion of control. 
Subtle dark circles under eyes hint at the coming struggle. Clean 
white background isolates the figure, emphasizing the solitude of 
survival. Panel 2: The same figure now hunched against a cracked 
concrete wall, uniform torn and soiled, hands clutching stomach in 
visible pain. Gaunt cheekbones emerge, eyes hollow. Empty ration 
wrappers scatter like fallen leaves at their feet. The background 
darkens, walls showing decay. Panel 3: Collapsed in fetal position 
on cold ground, barely conscious, one arm tucked under head. The 
uniform is now rags. More wrappers surround the figure like a 
desperate nest. Dark, abstract background with ghostly elements 
suggesting hallucinations or fading consciousness. Below: A simple 
line graph labeled 'ENERGY LEVEL OVER TIME' showing a steady, 
inevitable decline. Heavy cross-hatching throughout, dramatic 
lighting, gritty atmosphere, professional graphic novel style."
```

---

## Cost Estimation (OpenAI)

- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Per prompt**: ~500 tokens input + 200 tokens output = **~$0.0002 per prompt**
- **100 scenes**: ~$0.02 total
- **Very affordable** for production use

---

## Questions to Decide

1. **Which LLM provider?**
   - ✅ Start with OpenAI (easy, fast, cheap)
   - Add local LLM later if needed

2. **When to use LLM?**
   - ✅ Always (if `use_llm: true`)
   - ✅ Only if `visual_prompt` is missing
   - ✅ As enhancement to existing prompts

3. **Caching?**
   - Cache generated prompts to avoid re-generation?
   - Save to `complete_script.json` after generation?

4. **User control?**
   - Allow manual override?
   - Show generated prompt before using?

---

## Recommendation

**Start with DeepSeek API (FREE):**
- ✅ FREE tier available
- High quality, creative output
- Very affordable ($0.0002 per prompt)
- Easy to implement
- Can add Grok/OpenAI/local LLM later if needed

**Implementation priority:**
1. ✅ Add OpenAI prompt enhancement module
2. ✅ Integrate with `generate_complete_scenes.py`
3. ✅ Add config and flags
4. ⏸️ Add local LLM support (optional, later)

---

## Next Steps

1. **Confirm approach**: OpenAI API or local LLM?
2. **Review prompt template**: Does it match your vision?
3. **Test with one scene**: Generate sample creative prompt
4. **Iterate**: Refine based on results

