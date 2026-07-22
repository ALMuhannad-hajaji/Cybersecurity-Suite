import sys
import argparse
import secrets
import string
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

def generate_password(length: int = 16) -> str:
    """Generates a cryptographically secure random password guaranteeing all character classes."""
    if length < 8:
        logger.warning("Password length less than 8 is insecure. Automatically adjusting to 8.")
        length = 8

    alphabet = string.ascii_letters + string.digits + string.punctuation
    
    # Guarantee at least one of each character class
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # Fill the rest randomly
    password += [secrets.choice(alphabet) for _ in range(length - 4)]
    
    # Shuffle the list to prevent predictable placement of guaranteed characters
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def main():
    parser = argparse.ArgumentParser(description="Secure Password Generator")
    parser.add_argument("-l", "--length", type=int, help="Length of the password", default=16)
    
    args = parser.parse_args()
    
    if not sys.argv[1:]:
        try:
            length_input = input("Enter password length [16]: ").strip()
            length = int(length_input) if length_input else 16
        except ValueError:
            logger.error("Invalid integer. Using default length 16.")
            length = 16
    else:
        length = args.length

    password = generate_password(length)
    print("\n" + "="*40)
    print("SECURE PASSWORD GENERATOR")
    print("="*40)
    print(f"Password: {password}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
