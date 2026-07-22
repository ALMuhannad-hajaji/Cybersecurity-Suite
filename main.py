import os
import sys
import time
import pyfiglet
from colorama import init, Fore, Style

# Import tools
from sec_suite.scanners import net_scan, port_scan, packet_sniffer
from sec_suite.crypto import file_crypt, hash_checker
from sec_suite.analysis import log_analyzer, ai_phishing_detector
from sec_suite.tools import pass_gen, dir_buster

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    custom_fig = pyfiglet.Figlet(font='slant')
    ascii_banner = custom_fig.renderText('CYBERSECURITY\nSUITE MX')
    
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(Fore.YELLOW + "="*54)
    print(Fore.GREEN + Style.BRIGHT + "   Developed by AL MUHANNAD MOHAMMED MOHAMMED HAJAJI")
    print(Fore.YELLOW + "="*54 + "\n")

def menu():
    while True:
        display_banner()
        print(Fore.WHITE + Style.BRIGHT + "[1] Network Scanner")
        print("[2] Port Scanner")
        print("[3] Packet Sniffer")
        print("[4] File Encryptor")
        print("[5] Hash Checker")
        print("[6] Log Analyzer")
        print("[7] Password Generator")
        print("[8] AI Phishing Detector")
        print("[9] Directory Buster")
        print(Fore.RED + "[0] Exit\n")
        print(Fore.YELLOW + "="*54)
        
        choice = input(Fore.GREEN + "\nSelect an option [0-9]: " + Style.RESET_ALL).strip()
        
        if choice == '1':
            net_scan.main()
        elif choice == '2':
            port_scan.main()
        elif choice == '3':
            packet_sniffer.main()
        elif choice == '4':
            file_crypt.main()
        elif choice == '5':
            hash_checker.main()
        elif choice == '6':
            log_analyzer.main()
        elif choice == '7':
            pass_gen.main()
        elif choice == '8':
            ai_phishing_detector.main()
        elif choice == '9':
            dir_buster.main()
        elif choice == '0':
            print(Fore.CYAN + "\nExiting CYBERSECURITY SUITE. Goodbye!\n")
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid selection. Please choose a valid tool.")
            time.sleep(1)
            continue
            
        input(Fore.CYAN + "\nPress ENTER to return to the main menu..." + Style.RESET_ALL)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(Fore.RED + "Main execution requires no arguments for the dashboard.")
        print("To run specific tools, execute them directly, e.g.:")
        print("  python sec_suite/scanners/port_scan.py -h")
        sys.exit(1)
    
    try:
        menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Operation interrupted by user. Exiting.\n")
        sys.exit(0)
