import re
from urllib.parse import urlparse, unquote
from trust_layer import BRAND_DOMAINS

# -----------------------------
# CONFIG
# -----------------------------

TRUSTED_DOMAINS = set(BRAND_DOMAINS.values())

HIGH_RISK_TLDS = {"tk", "xyz", "ml", "cf", "gq", "top", "icu", "click", "site"}

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "lnkd.in", "rb.gy"}

SCAM_PATTERNS = [
    "offer-letter", "processing-fee", "security-deposit",
    "activation-fee", "caution-deposit", "refund"
]

RISK_KEYWORDS = {
    "job": 3, "jobs": 3, "career": 3, "careers": 3,
    "intern": 3, "internship": 3,
    "hiring": 2, "recruitment": 3,
    "offer": 4, "login": 3, "verify": 4,
    "payment": 4, "fee": 5, "update": 2
}

# -----------------------------
# HELPERS
# -----------------------------

def parse_hostname(hostname: str):
    hostname = hostname.lower().split(":")[0]
    parts = hostname.split(".")
    if len(parts) <= 2:
        return hostname, ""
    return ".".join(parts[-2:]), ".".join(parts[:-2])

# -----------------------------
# CORE ENGINE
# -----------------------------

def analyze_url(url: str) -> dict:
    if not url:
        return {"domain": "", "score": 0, "risk": "Safe", "triggered_rules": []}

    url = unquote(url.strip())
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    hostname = parsed.netloc.lower()

    if not hostname:
        return {"domain": "", "score": 0, "risk": "Safe", "triggered_rules": []}

    registered, subdomain = parse_hostname(hostname)
    domain_name = registered.split(".")[0]
    full_text = (hostname + " " + url).lower()
    tld = registered.split(".")[-1]

    triggered = []
    score = 0

    # -----------------------------
    # TRUSTED DOMAIN (HARD SAFE)
    # -----------------------------
    if registered in TRUSTED_DOMAINS:
        return {
            "domain": hostname,
            "score": 2,
            "risk": "Safe",
            "triggered_rules": ["Trusted Domain"]
        }

    # -----------------------------
    # 🚨 HARD OVERRIDE (FIX FOR YOUR PROBLEM)
    # -----------------------------
    if tld in HIGH_RISK_TLDS:
        if any(k in full_text for k in ["job", "career", "intern", "hiring", "apply"]):
            return {
                "domain": hostname,
                "score": 92,
                "risk": "High Risk",
                "triggered_rules": ["High-risk TLD + Job/Career Scam"]
            }

    # -----------------------------
    # BASELINE
    # -----------------------------
    score += 8
    triggered.append("Baseline unknown domain")

    # -----------------------------
    # STRUCTURE SIGNALS
    # -----------------------------
    if parsed.scheme == "http":
        score += 5
        triggered.append("No HTTPS")

    if re.match(r"^\d{1,3}(\.\d{1,3}){3}", hostname):
        score += 30
        triggered.append("IP Address")

    if registered in SHORTENERS:
        score += 15
        triggered.append("URL Shortener")

    if tld in HIGH_RISK_TLDS:
        score += 18
        triggered.append("Suspicious TLD")

    # -----------------------------
    # SCAM PATTERNS
    # -----------------------------
    for p in SCAM_PATTERNS:
        if p in full_text:
            score += 30
            triggered.append(f"Scam Pattern: {p}")
            break

    # -----------------------------
    # KEYWORDS
    # -----------------------------
    for k, v in RISK_KEYWORDS.items():
        if k in full_text:
            score += v
            triggered.append(f"keyword:{k}")

    # -----------------------------
    # BRAND ABUSE
    # -----------------------------
    for brand, official in BRAND_DOMAINS.items():
        if brand in hostname and registered != official:
            score += 35
            triggered.append("Brand Abuse")
            break

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    score = min(100, score)

    # -----------------------------
    # RISK BANDS
    # -----------------------------
    if score >= 70:
        risk = "High Risk"
    elif score >= 40:
        risk = "Medium Risk"
    elif score >= 15:
        risk = "Low Risk"
    else:
        risk = "Safe"

    return {
        "domain": hostname,
        "score": score,
        "risk": risk,
        "triggered_rules": triggered
    }