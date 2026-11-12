import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

text = input("Enter text: ")

token_ids = encoding.encode(text)
tokens = [encoding.decode([token_id]) for token_id in token_ids]

print("\nOriginal text:", text)
print("Tokens:", tokens)
print("Token IDs:", token_ids)
print("Token count:", len(token_ids))