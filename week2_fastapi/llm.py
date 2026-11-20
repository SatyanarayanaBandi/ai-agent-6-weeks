import os

from dotenv import load_dotenv
from google import genai


# Load the .env file from the Week 1 project root
load_dotenv("../.env")


class LLMWrapper:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    def generate(self, message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=message
        )

        return response.text

    def generate_stream(self, message: str):
        response = self.client.models.generate_content_stream(
            model="gemini-3.5-flash",
            contents=message
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    def summarize(self, conversation: str) -> str:
        prompt = f"""
Summarize the following conversation.

Keep important facts, user preferences, decisions,
important questions, and information needed to
continue the conversation.

Do not add information that is not present.

Conversation:

{conversation}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text