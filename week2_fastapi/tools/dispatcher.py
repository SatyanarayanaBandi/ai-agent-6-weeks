import json
from datetime import datetime

from tools.calculator import calculate
from tools.faq_lookup import faq_lookup


LOG_FILE = "tool_calls.log"


def log_tool_call(tool_name: str, arguments: dict, result):
    """
    Log every tool call with its name, arguments, and result.
    """

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "arguments": arguments,
        "result": result
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(log_entry)
            + "\n"
        )


def dispatch_tool(tool_name: str, arguments: dict):
    """
    Manually dispatch a tool call to the correct Python function.
    """

    if tool_name == "calculator":

        expression = arguments.get("expression")

        if not expression:
            raise ValueError("calculator requires 'expression'")

        result = calculate(expression)

    elif tool_name == "faq_lookup":

        question = arguments.get("question")

        if not question:
            raise ValueError("faq_lookup requires 'question'")

        result = faq_lookup(question)

    else:
        raise ValueError(f"Unknown tool: {tool_name}")

    log_tool_call(
        tool_name,
        arguments,
        result
    )

    return result


def dispatch_tool_call(tool_call: dict):
    """
    Execute a tool call represented as a dictionary.
    """

    tool_name = tool_call["name"]
    arguments = tool_call["arguments"]

    result = dispatch_tool(
        tool_name,
        arguments
    )

    return {
        "name": tool_name,
        "arguments": arguments,
        "result": result
    }