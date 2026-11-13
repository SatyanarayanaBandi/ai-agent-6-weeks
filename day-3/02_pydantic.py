from pydantic import BaseModel, Field, field_validator


class TicketResult(BaseModel):
    category: str = Field(description="Main issue category")
    priority: str = Field(description="Ticket priority")
    summary: str = Field(description="Short issue summary")
    recommended_action: str = Field(
        description="Recommended support action"
    )

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        allowed = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        if value not in allowed:
            raise ValueError(
                f"Priority must be one of: {', '.join(allowed)}"
            )

        return value


json_response = """
{
    "category": "Billing",
    "priority": "URGENT",
    "summary": "Customer was charged twice.",
    "recommended_action": "Investigate the duplicate transaction."
}
"""


result = TicketResult.model_validate_json(json_response)

print("Validated JSON:")
print(result)

print("\nCategory:", result.category)
print("Priority:", result.priority)
print("Summary:", result.summary)
print("Recommended action:", result.recommended_action)