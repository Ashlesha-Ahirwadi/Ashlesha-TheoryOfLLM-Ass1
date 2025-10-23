# utils.py  (Anthropic Messages API, modern version)
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_MODEL = os.getenv("MODEL", "claude-3-haiku-20240307")

if not ANTHROPIC_API_KEY:
    raise RuntimeError("❌ ANTHROPIC_API_KEY missing. Make sure it’s in your .env file.")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def call_anthropic(prompt_text, model=None, max_tokens=200, temperature=0.0):
    """
    Uses the Messages API (recommended).
    """
    model = model or DEFAULT_MODEL
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    print("Testing Claude connection...")
    out = call_anthropic("Say hello in one sentence.")
    print("Claude replied:", out.strip())

