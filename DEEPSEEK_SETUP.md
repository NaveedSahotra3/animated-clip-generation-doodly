# 🔑 DeepSeek API Setup

## Get Your API Key

1. **Visit**: https://api-docs.deepseek.com
2. **Sign up** or log in
3. **Navigate to**: Account Settings → API Key
4. **Generate** a new API key
5. **Copy** the key (starts with `sk-...`)

## Set the API Key

### Option 1: Environment Variable (Recommended)
```bash
export DEEPSEEK_API_KEY="sk-your-key-here"
```

Add to your `~/.zshrc` or `~/.bash_profile` to make it permanent:
```bash
echo 'export DEEPSEEK_API_KEY="sk-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2: Config File
Edit `config/generation_config.yaml`:
```yaml
llm:
  api_key: "sk-your-key-here"  # Add your key here
```

**Note:** Option 1 (environment variable) is more secure and recommended.

## Test the Setup

```bash
python3 scripts/enhance_prompt_with_llm.py
```

Should output:
```
Testing DeepSeek LLM integration...
API configured: True

Generating creative prompt...
Generated prompt: [your enhanced prompt]
```

## Usage

In `scripts/complete_script.json`, set:
```json
{
  "scene_number": 1,
  "use_llm": true,
  "creativity": 0.7,
  "voice_over": "...",
  "visual_prompt": "..."  // Optional base prompt
}
```

- `use_llm: true` - Enable LLM enhancement
- `creativity: 0.0-1.0` - How creative (0.0 = literal, 1.0 = very creative)
- `visual_prompt` - Optional base prompt to enhance

## Cost

- **FREE tier available**
- ~$0.0002 per prompt
- Very affordable for production use

