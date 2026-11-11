\# Day 1 - Provider Documentation Notes



\## 1. API Request

Our Python program sends a request to the Anthropic API through the Python SDK.



\## 2. Model

The model identifies which LLM should process the request.



\## 3. Messages

The API request contains messages such as user messages and can also include a system instruction.



\## 4. System Message

The system message provides instructions about the model's behavior or role.



\## 5. User Message

The user message contains the task or question we want the model to answer.



\## 6. Max Tokens

max\_tokens controls the maximum number of output tokens the model can generate.



\## 7. Temperature

Temperature controls the variation/randomness of the generated response.



\## 8. Response

The API response contains the generated content and other response information.



\## 9. Usage

The response usage information tells us how many input and output tokens were used.



\## 10. API Key

The API key authenticates our application when it accesses the API. It must be kept secret and should not be committed to Git.



\## 11. Security

The API key should be stored in an environment variable such as ANTHROPIC\_API\_KEY and kept out of Git using .gitignore.

