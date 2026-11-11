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

prompts = [
    "What is Docker?",
    """Explain Docker in about 50 words. Include what containers are,
why Docker is useful, and one simple example."""
]

for prompt in prompts:

    print("\n==============================")
    print("PROMPT:")
    print(prompt)
    print("==============================")

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
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