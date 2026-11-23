import json
from pathlib import Path


FAQ_FILE = Path(__file__).parent / "faq.json"


def faq_lookup(question: str) -> str:
    """
    Look up an answer from the FAQ JSON file.

    Matching is case-insensitive and ignores
    leading/trailing whitespace and a final question mark.
    """

    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        faq_data = json.load(file)

    normalized_question = question.strip().lower()

    # Remove a trailing question mark
    normalized_question = normalized_question.rstrip("?").strip()

    # Normalize FAQ keys in the same way
    normalized_faq_data = {}

    for key, value in faq_data.items():

        normalized_key = key.strip().lower()
        normalized_key = normalized_key.rstrip("?").strip()

        normalized_faq_data[normalized_key] = value

    answer = normalized_faq_data.get(normalized_question)

    if answer:
        return answer

    return "No matching FAQ was found."