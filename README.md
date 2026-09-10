# ScamGraph-AI
AI-Powered Multimodal Scam Investigation &amp; Attack-Chain Intelligence Platform
# ScamGraph AI

## AI-Powered Multimodal Scam Investigation & Attack-Chain Intelligence Platform

### Project Objective

ScamGraph AI is a software-based AI/ML platform designed to detect, investigate, explain, and correlate digital scams.

Unlike traditional systems that only classify content as "Scam" or "Safe", ScamGraph AI analyzes multiple digital artifacts and connects them to reconstruct potential scam attack chains.

The system will initially support:

* Text messages
* Screenshots/images
* URLs
* Phone numbers
* Email addresses
* UPI IDs
* Payment requests

The long-term system will combine NLP, OCR, machine learning, semantic embeddings, entity extraction, knowledge graphs, anomaly detection, and explainable AI.

---

# Phase 1 Requirements — MVP

## 1. Core Functionality

The Phase 1 system must allow a user to:

1. Enter a suspicious message.
2. Submit the message for analysis.
3. Preprocess the text.
4. Extract relevant scam indicators.
5. Classify the message using an ML model.
6. Calculate a risk score.
7. Determine the scam category.
8. Display reasons for the prediction.
9. Provide safe-action recommendations.

---

# 2. Frontend Requirements

### Technology

* React
* TypeScript
* Vite
* Tailwind CSS

### Required pages/components

#### Dashboard

The dashboard should contain:

* ScamGraph AI branding
* Short project description
* Message input box
* Analyze button
* Example scam messages
* Recent investigations section

Example:

```text
SCAMGRAPH AI

Understand the Scam. Don't Just Detect It.

[ Paste suspicious message here... ]

              [ ANALYZE ]

Example:
"Your bank account will be blocked today.
Complete KYC immediately."
```

---

## 3. Investigation Result Page

Display:

### Risk Score

```text
Risk Score: 91/100
Risk Level: CRITICAL
```

### Scam Type

Example:

```text
KYC / Phishing
```

### Detected Indicators

Example:

```text
✓ Urgency
✓ Fear
✓ Impersonation
✓ Credential request
✓ Suspicious link
```

### Explanation

Example:

```text
Why was this flagged?

1. The message creates urgency.
2. It requests immediate action.
3. It appears to impersonate an organization.
4. It contains a suspicious link.
5. It requests sensitive information.
```

### Recommendation

```text
Do not click suspicious links.
Do not share OTPs, passwords or PINs.
Verify the request through an official channel.
```

---

# 4. Backend Requirements

### Technology

* Python
* FastAPI
* REST API

Required endpoint:

```text
POST /analyze
```

### Input

```json
{
  "text": "Your bank account will be blocked. Complete KYC immediately."
}
```

### Output

```json
{
  "risk_score": 91,
  "risk_level": "CRITICAL",
  "scam_probability": 0.91,
  "scam_type": "KYC/Phishing",
  "indicators": [
    "Urgency",
    "Fear",
    "Impersonation",
    "Credential Request"
  ],
  "recommendation": "Do not interact with the message."
}
```

---

# 5. NLP Requirements

The NLP pipeline should perform:

```text
Input Text
    ↓
Text Cleaning
    ↓
Tokenization
    ↓
Feature Extraction
    ↓
Entity Extraction
    ↓
Scam-Language Detection
```

The system should detect patterns such as:

### Urgency

```text
Act immediately
Respond within 10 minutes
Complete this today
```

### Fear

```text
Your account will be blocked
Your account will be suspended
Legal action will be taken
```

### Reward manipulation

```text
You won ₹50,000
Congratulations
Claim your reward
```

### Credential harvesting

```text
Enter your OTP
Verify your password
Enter your PIN
```

### Payment pressure

```text
Pay immediately
Send ₹10 to activate
Complete payment now
```

---

# 6. Machine Learning Requirements

Phase 1 must contain an actual ML model.

### Baseline model

Implement:

```text
TF-IDF
   ↓
Logistic Regression
   ↓
Scam Probability
```

The model must output:

```text
P(Scam)
P(Safe)
```

Example:

```text
Scam Probability = 0.91
Safe Probability = 0.09
```

---

# 7. Dataset Requirements

Create a dataset containing:

```text
text
label
scam_type
```

Example:

```csv
text,label,scam_type
"Your account will be blocked",1,KYC
"Congratulations you won a prize",1,Lottery
"Click here to verify your bank account",1,Phishing
"Your order has been delivered",0,None
"Your class starts at 10 AM",0,None
```

The dataset should contain both legitimate and scam examples.

Sensitive real-world conversations, credentials, OTPs, passwords and private financial information must not be collected or stored.

---

# 8. Risk Scoring

The initial risk score should combine ML prediction and detected indicators.

Example:

```text
ML probability          → 70%
Urgency                 → +5
Credential request      → +10
Impersonation            → +10
Suspicious URL           → +5
```

Final:

```text
Risk Score = 91/100
```

Initial levels:

```text
0–30       LOW
31–60      MEDIUM
61–80      HIGH
81–100     CRITICAL
```

These thresholds should later be evaluated experimentally.

---

# 9. Entity Extraction

Phase 1 should begin supporting extraction of:

```text
Phone numbers
Email addresses
URLs
UPI IDs
Organization names
```

Example:

```text
"Contact 9876543210 or pay abc@upi.
Visit secure-example.com"
```

Output:

```json
{
  "phone_numbers": ["9876543210"],
  "upi_ids": ["abc@upi"],
  "urls": ["secure-example.com"]
}
```

---

# 10. Explainability Requirements

The system must not simply output:

```text
SCAM
```

It must explain the prediction.

The explanation should be generated from detected evidence.

Example:

```text
The message was flagged because:

✓ It creates urgency.
✓ It requests sensitive information.
✓ It contains a suspicious URL.
✓ It uses financial-account language.
```

---

# 11. Phase 1 Database

Use PostgreSQL or SQLite initially.

Store:

```text
Investigation ID
Input text
Timestamp
Risk score
Scam probability
Scam type
Detected indicators
Extracted entities
```

Do not store:

* Passwords
* OTPs
* PINs
* Unnecessary personal information

---

# 12. Testing Requirements

The project must contain tests for:

### Backend

```text
/analyze
```

### ML

```text
Scam prediction
Legitimate prediction
```

### NLP

```text
URL extraction
Phone extraction
UPI extraction
Email extraction
```

### Risk Engine

```text
Low risk
Medium risk
High risk
Critical risk
```

---

# 13. Phase 1 Acceptance Criteria

Phase 1 is considered complete when:

* [ ] React frontend runs successfully.
* [ ] FastAPI backend runs successfully.
* [ ] Frontend communicates with backend.
* [ ] User can enter a message.
* [ ] Backend preprocesses the message.
* [ ] ML model predicts scam probability.
* [ ] Risk score is generated.
* [ ] Scam category is displayed.
* [ ] Scam indicators are extracted.
* [ ] Entities can be extracted.
* [ ] Explanation is displayed.
* [ ] Safe recommendations are displayed.
* [ ] Investigation can be stored.
* [ ] Basic unit/API tests pass.
* [ ] Project can be run using documented setup instructions.

---

# 14. Future Phases

Phase 1 should be designed so that the following can be added without major architectural changes.

### Phase 2 — Multimodal Analysis

```text
Screenshot
    ↓
OCR
    ↓
Text Extraction
    ↓
NLP
```

### Phase 3 — URL Intelligence

```text
URL
 ↓
Domain Analysis
 ↓
Brand Impersonation
 ↓
Typosquatting
 ↓
URL Risk
```

### Phase 4 — Semantic Intelligence

```text
Sentence Transformers
        ↓
Embeddings
        ↓
Vector Database
        ↓
Semantic Similarity
```

### Phase 5 — ScamGraph

```text
Entities
   ↓
Neo4j
   ↓
Evidence Graph
   ↓
Attack Chain
```

### Phase 6 — Scam DNA

Create a behavioral/structural fingerprint for each scam.

```text
Target
+
Psychological tactics
+
Entities
+
Infrastructure
+
Attack sequence
```

### Phase 7 — Campaign Detection

```text
Messages
   ↓
Embeddings
   ↓
Clustering
   ↓
Related Scam Campaigns
```

### Phase 8 — Attack-Stage Prediction

Predict the likely next stage of a scam:

```text
Contact
 ↓
Manipulation
 ↓
Phishing
 ↓
Credential Theft
 ↓
Payment Fraud
```

### Phase 9 — AI Investigation Assistant

Allow users to ask:

```text
Why was this flagged?

Are there related scams?

What is the likely objective?

What might happen next?

What should I do?
```

---

# 15. Recommended Repository Structure

```text
scamgraph-ai/
│
├── frontend/
│
├── backend/
│   ├── api/
│   ├── ml/
│   ├── nlp/
│   ├── vision/
│   ├── url/
│   ├── graph/
│   ├── llm/
│   ├── models/
│   └── main.py
│
├── datasets/
│
├── notebooks/
│
├── tests/
│
├── docs/
│
├── .gitignore
├── README.md
├── requirements.txt
└── docker-compose.yml
```

---

# 16. Development Principle

The system must follow:

```text
Evidence
   ↓
Analysis
   ↓
ML Prediction
   ↓
Correlation
   ↓
Explanation
```

The LLM should **not be the sole source of truth**.

ML models, extracted entities, rules, URL analysis and graph relationships should provide the evidence, while the LLM can later convert that evidence into a human-readable investigation report.

---

# 17. Final Project Vision

The final system should evolve from:

```text
"Is this a scam?"
```

into:

```text
"What is happening?"

"Why is it suspicious?"

"What evidence supports this?"

"Which entities are connected?"

"Is this related to another scam?"

"What attack stage is this?"

"What is likely to happen next?"

"What should the user do?"
```

### Final positioning

> **ScamGraph AI — A multimodal AI-powered scam investigation platform that correlates digital evidence, reconstructs scam attack chains, identifies related campaigns, and generates explainable risk assessments.**
