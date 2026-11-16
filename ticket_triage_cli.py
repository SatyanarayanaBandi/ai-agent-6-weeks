import csv
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError, field_validator


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class TicketTriageResponse(BaseModel):
    category: str = Field(
        description="Main issue category"
    )

    priority: str = Field(
        description="Ticket priority"
    )

    summary: str = Field(
        description="Short summary of the issue"
    )

    recommended_action: str = Field(
        description="Recommended support action"
    )

    answer: str = Field(
        description="Clear answer to the customer issue"
    )

    sources: list[str] = Field(
        default_factory=list,
        description="Sources actually provided in the ticket"
    )

    actions_pending_approval: list[str] = Field(
        default_factory=list,
        description="Actions requiring human approval"
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

Analyze the support ticket and return ONLY valid JSON.

Return exactly these fields:

category
priority
summary
recommended_action
answer
sources
actions_pending_approval

RULES:

1. category:
Identify the main issue category.

2. priority:
Choose exactly one:
LOW, MEDIUM, HIGH, CRITICAL

3. summary:
Give a short and accurate summary.

4. recommended_action:
Recommend the next action for the support team.

5. answer:
Give a clear answer about the reported issue.

6. sources:
List only sources explicitly provided or mentioned in the ticket.
Do not invent sources.
If none are provided, return an empty list.

7. actions_pending_approval:
List actions that require human approval before execution.
Do not claim that an action has already been performed.

8. Do not invent:
Do not invent account numbers, transaction IDs, amounts,
dates, payment gateways, or other facts not present in the ticket.

TICKET:
{ticket}
"""


def clean_json_response(response_text):
    clean_response = response_text.strip()

    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]

    elif clean_response.startswith("```"):
        clean_response = clean_response[3:]

    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]

    return clean_response.strip()


def log_cost(response):
    usage = getattr(response, "usage_metadata", None)

    if usage is None:
        return

    input_tokens = getattr(
        usage,
        "prompt_token_count",
        0
    ) or 0

    output_tokens = getattr(
        usage,
        "candidates_token_count",
        0
    ) or 0

    total_tokens = getattr(
        usage,
        "total_token_count",
        0
    ) or 0

    # Cost rates are configurable through environment variables.
    # Values are USD per 1 million tokens.
    input_rate = float(
        os.getenv("INPUT_COST_PER_1M", "0")
    )

    output_rate = float(
        os.getenv("OUTPUT_COST_PER_1M", "0")
    )

    estimated_cost = (
        (input_tokens / 1_000_000) * input_rate
        + (output_tokens / 1_000_000) * output_rate
    )

    file_exists = os.path.exists("cost.csv")

    with open(
        "cost.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "input_tokens",
                "output_tokens",
                "total_tokens",
                "estimated_cost_usd"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            input_tokens,
            output_tokens,
            total_tokens,
            f"{estimated_cost:.8f}"
        ])

    print("\n--- USAGE ---")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Estimated cost: ${estimated_cost:.8f}")


def triage_ticket(ticket):
    prompt = build_prompt(ticket)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    clean_response = clean_json_response(response.text)

    result = TicketTriageResponse.model_validate_json(
        clean_response
    )

    log_cost(response)

    return result


def print_result(result):
    print("\n========================================")
    print("         TICKET TRIAGE RESULT")
    print("========================================")

    print("\nCategory:")
    print(result.category)

    print("\nPriority:")
    print(result.priority)

    print("\nSummary:")
    print(result.summary)

    print("\nRecommended Action:")
    print(result.recommended_action)

    print("\nAnswer:")
    print(result.answer)

    print("\nSources:")

    if result.sources:
        for source in result.sources:
            print("-", source)
    else:
        print("None provided.")

    print("\nActions Pending Approval:")

    if result.actions_pending_approval:
        for action in result.actions_pending_approval:
            print("-", action)
    else:
        print("None.")

    print("\n========================================")


def main():
    print("========================================")
    print("       AI TICKET TRIAGE ASSISTANT")
    print("========================================")

    ticket = input("\nEnter support ticket:\n> ").strip()

    if not ticket:
        print("Ticket cannot be empty.")
        return

    try:
        result = triage_ticket(ticket)
        print_result(result)

    except ValidationError as error:
        print("\n--- VALIDATION ERROR ---")
        print("The AI response did not match the required schema.")
        print(error)

    except ValueError as error:
        print("\n--- INVALID RESPONSE ERROR ---")
        print("The AI did not return valid JSON.")
        print(error)

    except Exception as error:
        print("\n--- APPLICATION ERROR ---")
        print(error)


if __name__ == "__main__":
    main()
