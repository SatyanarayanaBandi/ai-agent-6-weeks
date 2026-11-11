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
    """Explain the Python library quantumflowx.
Include its main purpose, installation command, and one example.""",

    """Explain the Python library quantumflowx.
If you are unsure whether this library exists, say that you are unsure.
Do not guess or invent information."""
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