import os
import sys

from dotenv import load_dotenv
import anthropic


SYSTEM_MESSAGE = "You are a helpful technical assistant. Explain clearly and briefly."
USER_MESSAGE = "Explain what Docker is in simple words."

MODEL = "claude-sonnet-5-5"
TEMPERATURE = 0.0
MAX_TOKENS = 500


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("Missing ANTHROPIC_API_KEY in .env")
    sys.exit(1)

client = anthropic.Anthropic(api_key=api_key)

print("Sending request...\n")

try:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=SYSTEM_MESSAGE,
        messages=[
            {
                "role": "user",
                "content": USER_MESSAGE
            }
        ],
    )

except Exception as e:
    print("API call failed:", e)
    sys.exit(1)


print("AI Response:\n")
print(response.content[0].text)
print()

print(f"Input tokens:  {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Stop reason:   {response.stop_reason}")