import sys
import os
import argparse
import shutil
from cryptography.fernet import Fernet
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

def generate_key() -> bytes:
    """Generates a new Fernet symmetric key."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    logger.info("New encryption key generated and saved as 'secret.key'")
    return key

def load_key(key_path: str = "secret.key") -> bytes:
    """Loads the encryption key from a file."""
    try:
        with open(key_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        logger.error(f"Key file '{key_path}' not found.")
        return b""

def process_file(file_path: str, key: bytes, encrypt: bool = True):
    """Encrypts or decrypts a file safely with an automatic backup."""
    if not os.path.exists(file_path):
        logger.error(f"Target file '{file_path}' does not exist.")
        return

    fernet = Fernet(key)
    backup_path = f"{file_path}.bak"
    
    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Backup created at '{backup_path}'")

        with open(file_path, "rb") as file:
            original_data = file.read()

        if encrypt:
            processed_data = fernet.encrypt(original_data)
            action = "encrypted"
        else:
            processed_data = fernet.decrypt(original_data)
            action = "decrypted"

        with open(file_path, "wb") as file:
            file.write(processed_data)
            
        logger.info(f"File '{file_path}' successfully {action}.")
        
    except Exception as e:
        logger.error(f"Process failed: {e}. Restoring from backup...")
        shutil.copy2(backup_path, file_path)
        logger.info("Rollback complete.")

def main():
    parser = argparse.ArgumentParser(description="File Encryptor/Decryptor")
    parser.add_argument("-f", "--file", help="Target file")
    parser.add_argument("-m", "--mode", choices=["enc", "dec", "gen"], help="Mode: enc, dec, gen")
    parser.add_argument("-k", "--key", help="Path to key file", default="secret.key")
    
    args = parser.parse_args()

    if not sys.argv[1:]:
        print("Modes: [1] Generate Key  [2] Encrypt File  [3] Decrypt File")
        mode_choice = input("Select mode: ").strip()
        if mode_choice == "1":
            generate_key()
            return
        elif mode_choice in ["2", "3"]:
            target_file = input("Enter file path: ").strip()
            key = load_key()
            if key:
                process_file(target_file, key, encrypt=(mode_choice == "2"))
    else:
        if args.mode == "gen":
            generate_key()
        elif args.mode in ["enc", "dec"] and args.file:
            key = load_key(args.key)
            if key:
                process_file(args.file, key, encrypt=(args.mode == "enc"))
        else:
            logger.error("Missing arguments. Use -h for help.")

if __name__ == "__main__":
    main()
