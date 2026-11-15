import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, field_validator

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class TicketResult(BaseModel):
    category: str = Field(description="Main issue category")
    priority: str = Field(description="Ticket priority")
    summary: str = Field(description="Short issue summary")
    recommended_action: str = Field(
        description="Recommended support action"
    )

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        allowed = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        if value not in allowed:
            raise ValueError(
                f"Priority must be one of: {', '.join(allowed)}"
            )

        return value


def build_prompt(ticket):
    return f"""
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

TICKET:
{ticket}
"""


ticket = input("Enter support ticket: ")

prompt = build_prompt(ticket)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("\n--- RAW GEMINI RESPONSE ---")
print(response.text)

result = TicketResult.model_validate_json(response.text)

print("\n--- VALIDATED RESULT ---")
print(result)

print("\nCategory:", result.category)
print("Priority:", result.priority)
print("Summary:", result.summary)
print("Recommended action:", result.recommended_action)