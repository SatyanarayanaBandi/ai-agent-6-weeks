import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def test_hallucination(ticket):
    prompt = f"""
You are a customer support assistant.

Analyze the ticket below.

IMPORTANT:
- Do not invent information.
- If information is not provided, say "Not provided".
- Do not guess account numbers, transaction amounts, or payment gateways.

Return exactly these fields:
account_number
amount
payment_gateway
summary

Return ONLY valid JSON.

TICKET:
{ticket}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    print("\n--- TICKET ---")
    print(ticket)

    print("\n--- MODEL RESPONSE ---")
    print(response.text.strip())


tickets = [
    "My payment failed but money was deducted.",
    "I was charged twice for my order.",
    "My account is locked after several login attempts."
]


for ticket in tickets:
    test_hallucination(ticket)