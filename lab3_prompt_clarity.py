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
    "Explain Docker.",
    """Explain Docker to a beginner.
Give exactly 3 bullet points.
Each bullet point must explain one important Docker concept.
Use simple language and one short example."""
]

for prompt in prompts:

    print("\n==============================")
    print("PROMPT:")
    print(prompt)
    print("==============================")

    response = client.messages.create(
        model=MODEL,
        max_tokens=250,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print("\nAI Response:")
    print(response.content[0].text)