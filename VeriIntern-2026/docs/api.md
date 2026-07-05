# API Reference

The backend exposes a compact FastAPI interface for risk analysis, URL inspection, payment detection, explainability, benchmarking, and health checks.

## Base URL

When running locally, the API is typically available at:

- http://localhost:8000

## Endpoints

### POST /analyze

Purpose
- Analyze internship posting text and optionally a URL.

Request
- JSON body with:
  - text: string
  - url: optional string

Response
- prediction, confidence, scam probability, final score, risk label, payment detection details, reasons, legitimate signals, explanation summary, and URL analysis when provided.

Example JSON

```json
{
  "prediction": "SCAM",
  "confidence": "HIGH",
  "scam_probability": 0.91,
  "final_score": 86.4,
  "risk_label": "HIGH RISK",
  "payment_detected": true,
  "matched_keywords": ["registration fee"],
  "negation_detected": false,
  "reasons": ["Payment demand detected (e.g. registration fee, caution deposit)."],
  "legitimate_signals": [],
  "explanation_summary": "Scam indicators detected (1 suspicious signal(s)).",
  "url_analysis": null
}
```

### POST /url

Purpose
- Evaluate the risk of a supplied URL.

Request
- JSON body with:
  - url: string

Response
- domain, raw score, score, risk, risk label, HTTPS status, domain trust, and trust flag.

Example JSON

```json
{
  "domain": "example-xyz.com",
  "raw_score": 3.68,
  "score": 92,
  "risk": "High Risk",
  "risk_label": "HIGH RISK",
  "https": true,
  "domain_trust": 0.3,
  "is_trusted": false
}
```

### POST /payment

Purpose
- Detect payment-related language in a posting.

Request
- JSON body with:
  - text: string

Response
- payment detection flag, matched keywords, keyword count, score, risk label, negation state, and matched negation phrases.

Example JSON

```json
{
  "payment_detected": true,
  "matched_keywords": ["registration fee"],
  "keyword_count": 1,
  "score": 20,
  "risk_label": "MEDIUM RISK",
  "negation_detected": false,
  "matched_negation": []
}
```

### POST /explain

Purpose
- Return a human-readable explanation of why a posting was classified as suspicious or legitimate.

Request
- JSON body with:
  - text: string

Response
- prediction, confidence, scam probability, suspicious signals, legitimate signals, explanation summary, reasons, reason count, verdict, and feature counts.

Example JSON

```json
{
  "prediction": "LEGITIMATE",
  "confidence": "MEDIUM",
  "scam_probability": 0.34,
  "suspicious_signals": [],
  "legitimate_signals": ["Official recruiter or hiring pipeline update context."],
  "explanation_summary": "Legitimate communication patterns detected (1 safe signal(s)).",
  "reasons": [],
  "reason_count": 0,
  "verdict": "This posting appears legitimate with 66.0% safe probability. Legitimate communication patterns detected (1 safe signal(s)).",
  "features": {
    "payment_signals": 0,
    "negation_detected": false
  }
}
```

### GET /benchmark

Purpose
- Run the built-in benchmark evaluation over the repository benchmark dataset.

Request
- No body.

Response
- Overall metrics and per-slice metrics for the benchmark dataset.

Example JSON

```json
{
  "overall": {
    "accuracy": 95,
    "precision": 98,
    "recall": 90.74,
    "fpr": 0
  },
  "slices": {},
  "total_samples": 1500
}
```

### GET /api/health

Purpose
- Confirm that the API service is running.

Request
- No body.

Response
- Service status and message.

Example JSON

```json
{
  "status": "ok",
  "message": "Internship Risk Analyzer API v2.0 is running"
}
```
