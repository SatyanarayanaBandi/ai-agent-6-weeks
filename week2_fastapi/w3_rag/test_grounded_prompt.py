import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv("../.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

PROMPT_FILE = Path(__file__).parent / "grounded_prompt.txt"


def load_prompt():
    return PROMPT_FILE.read_text(encoding="utf-8")


tests = [
    {
        "name": "Test 1 - Answer available",
        "context": "[source_id: company-001]\nThe company provides 20 days of annual paid leave for full-time employees.",
        "question": "How many days of annual paid leave does the company provide?",
    },
    {
        "name": "Test 2 - Answer unavailable",
        "context": "[source_id: company-002]\nThe company provides health insurance to eligible employees.",
        "question": "What is the company's maternity leave policy?",
    },
    {
        "name": "Test 3 - Multiple sources",
        "context": (
            "[source_id: product-001]\n"
            "The Basic plan costs $10 per month.\n\n"
            "[source_id: product-002]\n"
            "The Basic plan includes 10 projects."
        ),
        "question": "How much does the Basic plan cost and how many projects does it include?",
    },
    {
        "name": "Test 4 - Do not guess",
        "context": "[source_id: support-001]\nCustomer support is available from Monday to Friday.",
        "question": "What time does customer support open?",
    },
    {
        "name": "Test 5 - Preserve source_id",
        "context": "[source_id: policy-007]\nEmployees must complete security training within 30 days of joining the company.",
        "question": "When must employees complete security training?",
    },
]


def main():
    prompt_template = load_prompt()

    for test in tests:
        prompt = prompt_template.format(
            context=test["context"],
            question=test["question"],
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        print("=" * 70)
        print(test["name"])
        print("-" * 70)
        print("Question:", test["question"])
        print("Model Answer:")
        print(response.text)


if __name__ == "__main__":
    main()
