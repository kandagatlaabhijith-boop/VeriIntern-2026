# Design Decisions

## Why FastAPI

FastAPI was chosen because the project needed a lightweight API layer that could expose multiple analysis routes with minimal overhead. Its Python-first design fits the existing ML and text-processing modules well and makes the backend easy to extend.

## Why React

React was used for the interface because the application needed a responsive single-page experience for submitting posting text, reviewing analysis results, and viewing explanations. The existing React + Vite setup keeps the frontend lightweight and easy to iterate on.

## Why Logistic Regression

Logistic Regression was included as an interpretable baseline model for structured risk features. It is simple to train and easy to reason about, which makes it a useful complement to the more text-oriented model.

## Why Naive Bayes

Naive Bayes was selected for text classification because it performs well on token-based features and is straightforward to implement for the posting analysis use case. It provides a strong text-driven signal without adding significant complexity.

## Why Rule Engine

The rule engine is valuable because many fraud indicators are explicit and interpretable, such as payment demands, urgency words, and platform combinations. It offers transparent reasoning that users and reviewers can understand directly.

## Why Hybrid ML

The hybrid approach combines the transparency of a rule engine with the generalization capability of ML. This is especially useful in fraud detection, where some suspicious patterns are obvious while others are more subtle and context-dependent.

## Tradeoffs

- Rule-based logic is explainable but may miss novel phrasing.
- Classical ML models are practical and lightweight but depend on the quality of the training data.
- The hybrid design improves overall usefulness, though it requires careful calibration to avoid over-flagging legitimate content.
