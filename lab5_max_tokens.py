import os
import sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Missing ANTHROPIC_API_KEY in .env")
    sys.exit(1)

client = anthropic.Anthropic(api_key=api_key)

MODEL = "claude-sonnet-5-5"

prompt = """
Explain Docker in five detailed paragraphs.
Include containers, images, Dockerfiles, registries, and why Docker
is useful in software development.
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=20,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
)

print("\nAI Response:")
print(response.content[0].text)

print("\nToken Usage:")
print(f"Input tokens:  {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")

print(f"\nStop reason: {response.stop_reason}")