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
USER_MESSAGE = "Explain what Docker is in 2 sentences."

system_messages = [
    "You are a pirate. Explain things using pirate-style language.",
    "You are a senior software engineer. Explain things clearly in exactly 2 sentences.",
    "You are a helpful assistant. Explain things simply."
]

for system_message in system_messages:

    print("\n==============================")
    print("SYSTEM MESSAGE:")
    print(system_message)
    print("==============================")

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=system_message,
        messages=[
            {
                "role": "user",
                "content": USER_MESSAGE
            }
        ],
    )

    print("\nAI Response:")
    print(response.content[0].text)