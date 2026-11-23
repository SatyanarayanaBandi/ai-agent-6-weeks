from google.genai import types


CALCULATOR_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculator",
            description="Calculate a mathematical expression.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "expression": types.Schema(
                        type="STRING",
                        description="A mathematical expression such as 25 * 40."
                    )
                },
                required=["expression"]
            )
        )
    ]
)


FAQ_LOOKUP_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="faq_lookup",
            description="Look up an answer from the FAQ knowledge base.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "question": types.Schema(
                        type="STRING",
                        description="The FAQ question to look up."
                    )
                },
                required=["question"]
            )
        )
    ]
)


TOOLS = [
    CALCULATOR_TOOL,
    FAQ_LOOKUP_TOOL
]