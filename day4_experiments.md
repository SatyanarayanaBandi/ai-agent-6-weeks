# Week 1 Day 4 – Structured Outputs and Validation

## Objective
Build a reliable structured-response layer for an AI ticket triage application using Gemini and Pydantic.

## Topics Practiced
- Structured LLM responses
- JSON response design
- Pydantic BaseModel
- Pydantic Field
- Pydantic validation
- ValidationError handling
- Approval-required actions
- Preventing source hallucination
- Error handling for invalid LLM responses

## Structured Response Schema
The application expects exactly three fields:
- answer
- sources
- actions_pending_approval

## Practical Flow
User Ticket -> Prompt -> Gemini -> JSON Response -> JSON Cleanup -> Pydantic Validation -> Validated Structured Response -> CLI Output

## Test Results
1. Payment failure ticket - successful structured response.
2. Duplicate charge ticket - successful structured response.
3. Transaction reference ticket - no source was invented.
4. Invalid sources value - Pydantic rejected the invalid string.

## Error Handling
The Gemini application now handles Pydantic ValidationError, invalid JSON / ValueError, and unexpected application errors.

## Key Learning
Prompting asks the LLM for the required structure. Pydantic validates that structure before the application uses it.

## Day 4 Conclusion
The ticket triage application now produces structured responses and validates them before displaying the result. This makes the AI application more reliable and safer for downstream processing.
