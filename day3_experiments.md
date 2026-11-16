# Week 1 Day 3 — Prompt Engineering II, Sampling and Validation

## 1. Prompt Engineering II

Day 3 focused on improving prompts so the model produces more reliable and controlled responses.

### Techniques practiced

- Clear role definition
- Explicit output requirements
- Allowed-value constraints
- Structured JSON instructions
- Explicit "do not invent" rules
- Reusable prompt templates
- Validation after model output

### Example

Instead of:

> Analyze this ticket.

We used a more controlled instruction:

> You are a customer support ticket triage assistant.
> Choose exactly one priority:
> LOW, MEDIUM, HIGH, CRITICAL.
> Return only valid JSON with the required fields.

This reduces ambiguity and makes the output easier for the application to process.

---

## 2. Temperature and Sampling Experiment

Temperature was tested to understand how sampling affects model output.

### Temperature 0

Five runs produced:

```text
Run 1: Stashr
Run 2: Moneta
Run 3: Nudge
Run 4: Nest
Run 5: Vaulty