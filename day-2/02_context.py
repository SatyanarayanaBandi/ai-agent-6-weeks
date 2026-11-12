import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

system_message = "You are a helpful Java tutor."

user_messages = [
    "Explain inheritance in Java.",
    "Give a simple example.",
    "Explain method overriding.",
    "What is the difference between inheritance and composition?"
]

context = system_message

print("Initial context token count:",
      len(encoding.encode(context)))

for message in user_messages:
    context += "\n" + message

    token_count = len(encoding.encode(context))

    print("\nAdded message:", message)
    print("Current context token count:", token_count)