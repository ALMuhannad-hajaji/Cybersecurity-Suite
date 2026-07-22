import argparse
import socket
from concurrent.futures import ThreadPoolExecutor
from typing import List
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

def scan_port(target: str, port: int) -> int:
    """Attempts to connect to a specific port on the target."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except (socket.error, socket.timeout):
        pass
    except Exception as e:
        logger.error(f"Unexpected error on port {port}: {e}")
    return 0

def run_port_scan(target: str, start_port: int, end_port: int, threads: int = 100) -> List[int]:
    """Runs a multi-threaded port scan against a target."""
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        logger.error(f"Hostname resolution failed for {target}")
        return []

    logger.info(f"Starting port scan on {target_ip} ({start_port}-{end_port}) with {threads} threads")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port + 1)}
        for future in futures:
            port_result = future.result()
            if port_result:
                open_ports.append(port_result)
    
    return sorted(open_ports)

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Port Scanner")
    parser.add_argument("-t", "--target", dest="target", help="Target IP or Hostname")
    parser.add_argument("-p", "--ports", dest="ports", help="Port range (e.g. 1-1000)", default="1-1000")
    
    args = parser.parse_args()
    
    if not args.target:
        target = input("Enter target IP or Hostname: ").strip()
        port_range = input("Enter port range (e.g. 1-1000): ").strip() or "1-1000"
    else:
        target = args.target
        port_range = args.ports

    if target:
        try:
            start, end = map(int, port_range.split('-'))
            results = run_port_scan(target, start, end)
            
            print("\n" + "="*30)
            print(f"Open Ports on {target}")
            print("="*30)
            if results:
                for p in results:
                    print(f"[+] Port {p}: OPEN")
            else:
                print("[-] No open ports found.")
            print("="*30 + "\n")
        except ValueError:
            logger.error("Invalid port range format. Use Start-End (e.g. 1-100)")
        except KeyboardInterrupt:
            logger.info("Scan aborted by user.")

if __name__ == "__main__":
    main()
