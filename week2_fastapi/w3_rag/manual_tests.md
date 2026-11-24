# W3 RAG Grounded Prompt - Manual Tests

## Test 1: Answer available

### Context
[source_id: company-001]
The company provides 20 days of annual paid leave for full-time employees.

### Question
How many days of annual paid leave does the company provide?

### Expected Answer
The company provides 20 days of annual paid leave for full-time employees. [company-001]

---

## Test 2: Answer unavailable

### Context
[source_id: company-002]
The company provides health insurance to eligible employees.

### Question
What is the company's maternity leave policy?

### Expected Answer
The information is not available in the supplied context.

---

## Test 3: Multiple sources

### Context
[source_id: product-001]
The Basic plan costs $10 per month.

[source_id: product-002]
The Basic plan includes 10 projects.

### Question
How much does the Basic plan cost and how many projects does it include?

### Expected Answer
The Basic plan costs $10 per month and includes 10 projects. [product-001] [product-002]

---

## Test 4: Do not guess

### Context
[source_id: support-001]
Customer support is available from Monday to Friday.

### Question
What time does customer support open?

### Expected Answer
The information is not available in the supplied context.

---

## Test 5: Preserve source_id

### Context
[source_id: policy-007]
Employees must complete security training within 30 days of joining the company.

### Question
When must employees complete security training?

### Expected Answer
Employees must complete security training within 30 days of joining the company. [policy-007]
