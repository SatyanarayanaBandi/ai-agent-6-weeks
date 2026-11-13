# Day 3 Experiments

## Sampling Experiment

### Prompt

Give one short creative name for a personal finance application.

Return only the name.

### Temperature 0

Run 1: Stashr  
Run 2: Moneta  
Run 3: Nudge  
Run 4: Nest  
Run 5: Vaulty  

### Temperature 1

Run 1: Pelt  
Run 2: Pocketsync  
Run 3: Pocketsy  
Run 4: WalletWise  
Run 5: Nudge  

### Observation

Temperature 0 produced 5 different outputs in this experiment.

Temperature 1 also produced 5 different outputs.

The temperature 1 results showed more variation in style and naming,
although temperature 0 was also variable.

### Conclusion

1. Temperature affects the sampling behavior of the model.
2. Lower temperature does not guarantee identical outputs.
3. Higher temperature can allow more varied responses.
4. The same prompt can produce multiple valid outputs.
5. Temperature should be selected according to the application's requirements.
## Pydantic Validation

Pydantic was used to validate the JSON response from the LLM.

The `TicketResult` model contains:
- category
- priority
- summary
- recommended_action

`model_validate_json()` successfully converted valid JSON into a validated Pydantic object.

A priority validator was also added.

Valid priorities:
- LOW
- MEDIUM
- HIGH
- CRITICAL

An invalid priority such as `URGENT` was correctly rejected by Pydantic.

## Hallucination Trap Tests

Three tests were performed to check whether the model would invent missing information.

### Test 1
Ticket:
"My payment failed but money was deducted."

Missing information:
- Account number
- Amount
- Payment gateway

Result:
The model returned "Not provided" for all missing fields.

### Test 2
Ticket:
"I was charged twice for my order."

Missing information:
- Account number
- Amount
- Payment gateway

Result:
The model returned "Not provided" for all missing fields.

### Test 3
Ticket:
"My account is locked after several login attempts."

Missing information:
- Account number
- Amount
- Payment gateway

Result:
The model returned "Not provided" for all missing fields.

### Conclusion

The prompt successfully reduced hallucination by explicitly instructing the model not to invent missing information.

## Gemini + Pydantic Integration

Gemini was connected with Pydantic validation.

Flow:

User Ticket
→ Prompt Template
→ Gemini API
→ JSON Response
→ Pydantic Validation
→ Validated TicketResult

A real payment ticket was tested successfully.

The Gemini response was successfully validated by the `TicketResult` Pydantic model.

## Final Day 3 Conclusions

1. Temperature affects model sampling behavior and response variability.
2. Lower temperature does not guarantee identical outputs.
3. Reusable prompt templates make prompts easier to maintain.
4. Pydantic validates LLM-generated structured data before application use.
5. Explicit instructions can reduce hallucination, but validation remains important.