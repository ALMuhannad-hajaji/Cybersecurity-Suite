import sys
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

# Fallback minimal wordlist for demonstration
DEFAULT_WORDLIST = ["admin", "login", "dashboard", "api", "config", "backup", ".env", "test"]

def check_url(url: str):
    """Checks the HTTP status of a specific URL endpoint."""
    try:
        response = requests.get(url, timeout=3, allow_redirects=False)
        if response.status_code in [200, 301, 302, 403]:
            return url, response.status_code
    except requests.RequestException:
        pass
    return None

def run_dir_buster(base_url: str, wordlist: list, threads: int = 10):
    """Executes a directory brute-force attack (educational context)."""
    if not base_url.endswith("/"):
        base_url += "/"

    logger.info(f"Starting directory enumeration on {base_url} with {threads} threads")
    found = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        urls_to_check = [base_url + word.strip() for word in wordlist if word.strip()]
        results = executor.map(check_url, urls_to_check)

        for result in results:
            if result:
                url, status = result
                found.append(result)
                print(f"[+] Found: {url} (Status: {status})")

    return found

def main():
    parser = argparse.ArgumentParser(description="Directory Buster")
    parser.add_argument("-u", "--url", help="Target Base URL (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", help="Path to custom wordlist txt file")
    
    args = parser.parse_args()
    
    if not sys.argv[1:]:
        url = input("Enter target URL (e.g. http://example.com): ").strip()
        wordlist_path = input("Enter path to wordlist (leave empty for default short list): ").strip()
    else:
        url = args.url
        wordlist_path = args.wordlist

    if url:
        if not url.startswith("http"):
            url = "http://" + url
            
        words = DEFAULT_WORDLIST
        if wordlist_path:
            try:
                with open(wordlist_path, "r") as f:
                    words = f.readlines()
            except FileNotFoundError:
                logger.error("Wordlist file not found, using default.")
                
        print("\n" + "="*40)
        run_dir_buster(url, words)
        print("="*40 + "\n")

if __name__ == "__main__":
    main()
