from pydantic import BaseModel, Field, ValidationError

class StructuredResponse(BaseModel):
    answer: str = Field(description="Clear answer to the user")
    sources: list[str] = Field(default_factory=list)
    actions_pending_approval: list[str] = Field(default_factory=list)

invalid_data = {
    "answer": "Payment requires investigation.",
    "sources": "Payment Gateway",
    "actions_pending_approval": []
}

print("--- VALIDATION TEST ---")

try:
    result = StructuredResponse.model_validate(invalid_data)
    print("Validation successful:")
    print(result)

except ValidationError as error:
    print("Validation failed:")
    print(error)
