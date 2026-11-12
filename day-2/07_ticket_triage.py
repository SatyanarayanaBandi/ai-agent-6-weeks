import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_ticket(ticket):
    prompt = f"""
You are a customer support ticket triage assistant.

Analyze the following support ticket.

CATEGORY:
Identify the main issue category.

PRIORITY:
Choose exactly one:
LOW, MEDIUM, HIGH, CRITICAL.

SUMMARY:
Give a short summary of the customer's issue.

RECOMMENDED ACTION:
Recommend the next action that the support team should take.

IMPORTANT:
Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside the JSON.

Return exactly these fields:
category
priority
summary
recommended_action

Example:
{{
    "category": "Payment",
    "priority": "HIGH",
    "summary": "Payment failed but money was deducted.",
    "recommended_action": "Investigate the transaction and process a reversal if required."
}}

TICKET:
{ticket}
"""

    # Send prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # Clean possible Markdown formatting
    clean_response = response.text.strip()

    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]

    if clean_response.startswith("```"):
        clean_response = clean_response[3:]

    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]

    # Convert JSON text into Python dictionary
    return json.loads(clean_response.strip())


# Get ticket from user
ticket = input("Enter support ticket: ")

# Classify ticket
result = classify_ticket(ticket)

# Display result
print("\n--- TRIAGE RESULT ---")
print(json.dumps(result, indent=2))