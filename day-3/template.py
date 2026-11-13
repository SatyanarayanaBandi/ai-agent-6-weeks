def build_ticket_prompt(ticket):
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


if __name__ == "__main__":
    ticket = input("Enter support ticket: ")

    prompt = build_ticket_prompt(ticket)

    print("\n--- GENERATED PROMPT ---")
    print(prompt)