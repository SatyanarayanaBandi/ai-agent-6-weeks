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
Explain what Kubernetes is in exactly 3 simple sentences.
"""

for temperature in [0.0, 1.0]:
    print("\n==============================")
    print(f"Temperature: {temperature}")
    print("==============================")

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print(response.content[0].text)