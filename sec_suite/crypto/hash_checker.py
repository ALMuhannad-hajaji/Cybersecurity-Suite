import hashlib
import argparse
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)


def compute_hash(file_path: str, algo: str = "sha256") -> str:
    """
    Compute the hash of a file.

    Supported algorithms:
        - md5
        - sha1
        - sha256
    """
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
        }

        algo = algo.lower()

        if algo not in algorithms:
            raise ValueError(f"Unsupported algorithm: {algo}")

        hasher = algorithms[algo]()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        return ""

    except Exception as e:
        logger.error(f"Error: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(description="File Hash Checker")

    parser.add_argument(
        "file",
        nargs="?",
        help="File to hash"
    )

    parser.add_argument(
        "-a",
        "--algo",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm"
    )

    parser.add_argument(
        "-e",
        "--expected",
        help="Expected hash for comparison"
    )

    args = parser.parse_args()

    file_path = args.file or input("Enter file path: ").strip()
    algo = args.algo
    expected = args.expected

    file_hash = compute_hash(file_path, algo)

    if not file_hash:
        return

    print("\n" + "=" * 50)
    print(f"File: {file_path}")
    print(f"Algorithm: {algo.upper()}")
    print(f"Hash: {file_hash}")

    if expected:
        if file_hash.lower() == expected.lower():
            print("Status: MATCH")
        else:
            print("Status: NOT MATCH")

    print("=" * 50)


if __name__ == "__main__":
    main()