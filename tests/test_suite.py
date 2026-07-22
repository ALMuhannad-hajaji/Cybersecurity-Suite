import os
import pytest

from sec_suite.tools.pass_gen import generate_password
from sec_suite.analysis.ai_phishing_detector import analyze_email
from sec_suite.crypto.hash_checker import compute_hash


def test_password_generator_length():
    """Test that the password generator respects length inputs."""
    pwd_16 = generate_password(16)
    assert len(pwd_16) == 16

    pwd_short = generate_password(4)  # Should auto-adjust to 8
    assert len(pwd_short) == 8


def test_password_generator_complexity():
    """Test that generated passwords contain required character classes."""
    pwd = generate_password(20)

    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_punct = any(not c.isalnum() for c in pwd)

    assert has_upper
    assert has_lower
    assert has_digit
    assert has_punct


def test_phishing_detector_safe():
    """Test the phishing detector against benign text."""
    safe_text = "Hi team, let's meet at 10 AM to discuss the project architecture."

    risk, score, reasons = analyze_email(safe_text)

    assert risk == "LOW"
    assert score == 0
    assert len(reasons) == 0


def test_phishing_detector_malicious():
    """Test the phishing detector against heuristic indicators."""
    phishing_text = (
        "Urgent: Verify your account immediately by clicking "
        "this secure-login link to update your billing."
    )

    risk, score, reasons = analyze_email(phishing_text)

    assert risk == "HIGH"
    assert score >= 4
    assert len(reasons) > 0


def test_hash_checker():
    """Test file hashing utility functions."""

    test_file = "test_data.txt"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("cybersecurity")

    md5_hash = compute_hash(test_file, "md5")
    sha256_hash = compute_hash(test_file, "sha256")

    assert md5_hash == "b03a894e101746d09277f1f255cc8a40"

    # Updated SHA-256 value
    assert sha256_hash == (
        "64a1e1972b663b35a8c06b453ce018251efef00925fb414217f6087f179031b8"
    )

    if os.path.exists(test_file):
        os.remove(test_file)