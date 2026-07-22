import argparse
from typing import Tuple, List
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

# Rule-based Phishing Heuristics Engine
PHISHING_INDICATORS = {
    "urgent_language": ["urgent", "immediately", "account suspended", "action required", "within 24 hours"],
    "credential_requests": ["password", "verify your account", "login to continue", "update your billing"],
    "financial_requests": ["wire transfer", "invoice attached", "payment details", "gift card", "crypto"],
    "suspicious_urls": ["bit.ly", "tinyurl", "login-", "secure-", "update-", "verify-"],
}

def analyze_email(content: str) -> Tuple[str, int, List[str]]:
    """Analyzes text based on heuristics to determine phishing probability."""
    content_lower = content.lower()
    score = 0
    reasons = []

    for category, keywords in PHISHING_INDICATORS.items():
        for keyword in keywords:
            if keyword in content_lower:
                score += 1
                reasons.append(f"Contains {category.replace('_', ' ')} indicator: '{keyword}'")

    if score >= 4:
        risk = "HIGH"
    elif score >= 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, score, reasons

def main():
    parser = argparse.ArgumentParser(description="Rule-Based Phishing Text Detector")
    parser.add_argument("-t", "--text", help="Email body text to analyze")
    
    args = parser.parse_args()
    
    text = args.text
    if not text:
        print("Enter the email content to analyze (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        text = "\n".join(lines)

    if text.strip():
        logger.info("Analyzing text through heuristic engine...")
        risk, score, reasons = analyze_email(text)
        
        print("\n" + "="*50)
        print("PHISHING ANALYSIS REPORT")
        print("="*50)
        print(f"Risk Level : {risk}")
        print(f"Risk Score : {score}")
        print("-" * 50)
        if reasons:
            print("Triggered Heuristics:")
            for reason in set(reasons):
                print(f"  [!] {reason}")
        else:
            print("  [+] No malicious indicators found.")
        print("="*50 + "\n")
    else:
        logger.warning("No text provided.")

if __name__ == "__main__":
    main()
