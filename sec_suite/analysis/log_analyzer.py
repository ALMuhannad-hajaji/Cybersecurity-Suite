import re
import argparse
from collections import Counter
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

def analyze_logs(log_file: str) -> dict:
    """Analyzes authentication logs and returns statistics of failed attempts."""
    failed_ips = Counter()
    
    # Common Linux auth.log failure patterns
    patterns = [
        r"Failed password for .* from (?P<ip>\d+\.\d+\.\d+\.\d+)",
        r"authentication failure; .* rhost=(?P<ip>\d+\.\d+\.\d+\.\d+)",
        r"Invalid user .* from (?P<ip>\d+\.\d+\.\d+\.\d+)"
    ]
    
    try:
        with open(log_file, "r") as file:
            for line in file:
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        failed_ips[match.group("ip")] += 1
                        break
        return failed_ips
    except FileNotFoundError:
        logger.error(f"Log file '{log_file}' not found.")
        return {}
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Authentication Log Analyzer")
    parser.add_argument("-f", "--file", help="Path to auth.log file")
    
    args = parser.parse_args()
    
    log_file = args.file if args.file else input("Enter path to log file (e.g., /var/log/auth.log): ").strip()
    
    if log_file:
        logger.info(f"Analyzing {log_file} for malicious authentication attempts...")
        results = analyze_logs(log_file)
        
        if results:
            print("\n" + "="*40)
            print("Suspicious IPs\t\tFailed Attempts")
            print("="*40)
            for ip, count in results.most_common(15):
                print(f"{ip}\t\t{count}")
            print("="*40 + "\n")
        else:
            logger.info("No suspicious authentication failures detected or file is empty.")

if __name__ == "__main__":
    main()
