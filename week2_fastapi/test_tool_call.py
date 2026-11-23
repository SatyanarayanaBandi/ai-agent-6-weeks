from llm import LLMWrapper
from tools.tool_definitions import TOOLS
from tools.dispatcher import dispatch_tool_call


llm = LLMWrapper()

user_message = "What is 25 multiplied by 40? Use the calculator tool."

result = llm.generate_with_tool_loop(
    message=user_message,
    tools=TOOLS,
    dispatch_tool_call=dispatch_tool_call
)

print("FINAL MODEL ANSWER:")
print(result["answer"])

print("\nTOOL CALLS:")

for tool_call in result["tool_calls"]:
    print("Tool:", tool_call["name"])
    print("Arguments:", tool_call["arguments"])
    print("Result:", tool_call["result"])