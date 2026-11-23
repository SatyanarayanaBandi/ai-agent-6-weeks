import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    def generate_with_tools(self, message: str, tools: list):
        """
        Generate a response using available function tools.

        The model may return a function call.
        Our application is responsible for executing the tool.
        """

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                tools=tools
            )
        )

        return response

    def generate_with_tool_loop(
        self,
        message: str,
        tools: list,
        dispatch_tool_call
    ) -> dict:
        """
        Execute the complete model -> tool -> result -> model loop.

        Returns:
            {
                "answer": final model answer,
                "tool_calls": [...]
            }
        """

        response = self.generate_with_tools(
            message,
            tools
        )

        tool_calls = []

        # If the model does not request a tool,
        # return its normal response.
        if not response.function_calls:

            return {
                "answer": response.text,
                "tool_calls": []
            }

        # Execute each requested tool call.
        for function_call in response.function_calls:

            tool_call = {
                "name": function_call.name,
                "arguments": dict(function_call.args)
            }

            tool_result = dispatch_tool_call(
                tool_call
            )

            tool_calls.append(
                tool_result
            )

        # Build function-response parts.
        function_response_parts = []

        for tool_call in tool_calls:

            function_response_parts.append(
                types.Part.from_function_response(
                    name=tool_call["name"],
                    response={
                        "result": tool_call["result"]
                    }
                )
            )

        # Send the tool results back to Gemini.
        tool_response = types.Content(
            role="user",
            parts=function_response_parts
        )

        final_response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=message
                        )
                    ]
                ),
                response.candidates[0].content,
                tool_response
            ],
            config=types.GenerateContentConfig(
                tools=tools
            )
        )

        return {
            "answer": final_response.text,
            "tool_calls": tool_calls
        }