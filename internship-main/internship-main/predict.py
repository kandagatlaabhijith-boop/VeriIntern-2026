# ============================================================
#  STANDALONE PREDICTION SCRIPT
#  v1.2: Negation-aware pipeline
#  Run: python predict.py
# ============================================================

from part2_ml_model import EnsembleModel
from url_checker import analyze_url
from payment_detector import detect_payment, detect_negation
from explainability import explain_prediction
from trust_layer import get_domain_trust

model = EnsembleModel()
model.train()

sample_url = "http://tcs-careers-login-verify.xyz"

sample_text = """
TCS Internship Opportunity

Urgent hiring for Cyber Security role.

To proceed, pay a registration fee of ₹999 to confirm your slot.

Limited seats available. Apply immediately.

Contact: support@tcs-careers.xyz
"""


prediction = model.predict(sample_text)
url_result = analyze_url(sample_url)
payment_result = detect_payment(sample_text)
negation_result = detect_negation(sample_text)
explanation = explain_prediction(sample_text)

domain_trust = get_domain_trust(url_result['domain'])

# ── Fusion Layer (matches main.py) ──────────────────────────
ml_score = prediction['scam_probability'] * 100
domain_score = float(url_result['score'])

# rules_score approximation for standalone script
rules_score = 0.0
if payment_result['payment_detected'] and not negation_result['negation_detected']:
    rules_score += 70
if negation_result['negation_detected']:
    rules_score = min(rules_score, 10)
rules_score = max(0.0, min(100.0, rules_score))

if sample_url:
    final_score = 0.4 * rules_score + 0.4 * ml_score + 0.2 * domain_score
else:
    final_score = 0.5 * rules_score + 0.5 * ml_score

# Negation override
if negation_result['negation_detected']:
    final_score = min(final_score, 14.0)

final_score = max(0.0, min(100.0, final_score))

if final_score >= 75:
    final_risk = "HIGH RISK"
elif final_score >= 40:
    final_risk = "MEDIUM RISK"
else:
    final_risk = "LOW RISK"


print("\n===== FINAL FRAUD ANALYSIS =====\n")

print(f"prediction       : {prediction['prediction']}")
print(f"confidence       : {prediction['confidence']}")
print(f"scam_probability : {prediction['scam_probability']}")

print(f"\ndomain           : {url_result['domain']}")
print(f"risk             : {url_result['risk']}")

print(f"\npayment_detected : {payment_result['payment_detected']}")
print(f"matched_keywords : {payment_result['matched_keywords']}")
print(f"negation_detected: {negation_result['negation_detected']}")

print("\nSuspicious Signals:")
for r in explanation['suspicious_signals']:
    print(f"  [!] {r}")

print("\nLegitimate Signals:")
for r in explanation['legitimate_signals']:
    print(f"  [+] {r}")

print(f"\nExplanation: {explanation['summary']}")

print("\n===== FINAL DECISION =====\n")

print(f"Final Risk Score : {final_score:.2f}")
print(f"Final Risk Level : {final_risk}")


# ── Test negation handling ──────────────────────────────────
print("\n\n===== NEGATION HANDLING TESTS =====\n")

negation_tests = [
    "No payment required",
    "No registration fee required",
    "Fee waived",
    "Free internship program",
    "There is no payment required",
]

for test_text in negation_tests:
    pred = model.predict(test_text)
    pay = detect_payment(test_text)
    neg = detect_negation(test_text)
    expl = explain_prediction(test_text)

    score = pred['scam_probability'] * 50
    if pay['payment_detected']:
        score += 20
    if neg['negation_detected']:
        score = max(0, score - 20)
    score = max(0, min(100, score))

    status = "PASS" if score < 15 and pred['scam_probability'] < 0.30 else "FAIL"

    print(f"  [{status}] \"{test_text}\"")
    print(f"    prediction={pred['prediction']} scam_prob={pred['scam_probability']:.3f} score={score:.1f}")
    print(f"    payment={pay['payment_detected']} negation={neg['negation_detected']}")
    if expl['legitimate_signals']:
        print(f"    legit_signals: {expl['legitimate_signals'][:2]}")
    print()