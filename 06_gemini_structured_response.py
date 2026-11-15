import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class StructuredResponse(BaseModel):
    answer: str = Field(
        description="Clear answer to the user"
    )

    sources: list[str] = Field(
        default_factory=list,
        description="Sources used to support the answer"
    )

    actions_pending_approval: list[str] = Field(
        default_factory=list,
        description="Actions that require approval"
    )


def build_prompt(ticket):
    return f"""
You are a customer support ticket triage assistant.

Analyze the user's ticket.

Return ONLY valid JSON.

Return exactly these fields:

answer
sources
actions_pending_approval

RULES:

1. answer:
Give a clear and concise answer about the issue.

2. sources:
List only sources actually provided or mentioned in the ticket.
Do not invent sources.
If no sources are provided, return an empty list.

3. actions_pending_approval:
List actions that require human approval before execution.
Do not claim that an action has already been performed.

TICKET:
{ticket}
"""


ticket = input("Enter support ticket: ")

prompt = build_prompt(ticket)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    print("\n--- RAW GEMINI RESPONSE ---")
    print(response.text)

    clean_response = response.text.strip()

    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]

    if clean_response.startswith("```"):
        clean_response = clean_response[3:]

    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]

    clean_response = clean_response.strip()

    result = StructuredResponse.model_validate_json(
        clean_response
    )

    print("\n--- VALIDATED STRUCTURED RESPONSE ---")

    print("\nAnswer:")
    print(result.answer)

    print("\nSources:")
    for source in result.sources:
        print("-", source)

    print("\nActions Pending Approval:")
    for action in result.actions_pending_approval:
        print("-", action)

except ValidationError as error:
    print("\n--- VALIDATION ERROR ---")
    print("Gemini returned data that does not match the required schema.")
    print(error)

except ValueError as error:
    print("\n--- INVALID RESPONSE ERROR ---")
    print("Gemini did not return valid JSON.")
    print(error)

except Exception as error:
    print("\n--- APPLICATION ERROR ---")
    print("An unexpected error occurred.")
    print(error)
