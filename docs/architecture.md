# Architecture

## Problem Statement

VeriIntern helps identify likely internship fraud by combining text analysis, URL risk checks, and explainable scoring. The system is designed to flag suspicious internship postings that ask for fees, use urgent language, or route applicants through risky domains.

## System Flow

1. A user submits posting text and an optional URL.
2. The backend normalizes the text and extracts structured features such as payment language, urgency, platform references, and onboarding context.
3. A rule engine produces an initial risk score from heuristic signals.
4. An ML engine evaluates the same input using a Naive Bayes classifier and a Logistic Regression classifier.
5. The fusion layer combines rule, ML, and URL-based signals into a final score.
6. The explanation layer returns human-readable reasons for the prediction.

## ML Engine

The ML engine is implemented in the repository as an ensemble model built from:

- Naive Bayes for token-based text likelihood
- Logistic Regression for feature-based scoring

The model is trained from the repository datasets during startup and produces a scam probability for incoming text.

## Rule Engine

The rule engine is driven by feature extraction from the dataset similarity module. It looks for:

- payment demands
- negation-aware fee statements
- urgency phrases
- telegram/WhatsApp communication cues
- legitimate recruiter or onboarding context

These rules produce a score that can be adjusted by contextual signals.

## URL Analysis

The URL analysis module inspects domains and URL structure for suspicious patterns such as shorteners, risky TLDs, suspicious keywords, and impersonation indicators. Domain trust is also evaluated using a simple trust layer.

## Fusion Layer

The backend combines:

- rule-based score
- ML scam probability
- URL/domain score

The final score is capped to the 0-100 range, and the resulting label is mapped to LOW, MEDIUM, or HIGH RISK.

## Explainability Layer

The explainability module turns detected features into readable signals. It separates suspicious cues from legitimate ones and provides a summary message that can be surfaced to users.

## Tradeoffs

- The rule engine is transparent and easy to reason about, but it depends on carefully curated phrases.
- The ML component improves generalization, but it is still tied to the training dataset and feature set.
- The hybrid design balances interpretability and predictive power, though it may still require human review for borderline cases.

## Future Improvements

Potential next steps include broader evaluation, richer URL analysis, better explainability output, and more deployment-focused infrastructure such as Docker, CI/CD, and observability.
