import argparse
import sys
from typing import List, Dict
import scapy.all as scapy
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)

def scan_network(ip_range: str) -> List[Dict[str, str]]:
    """Scans the network using ARP requests."""
    logger.info(f"Initiating ARP scan for IP range: {ip_range}")
    try:
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        clients_list = []
        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            clients_list.append(client_dict)
        return clients_list
    except PermissionError:
        logger.error("Permission denied. Network sniffing requires root/administrator privileges.")
        return []
    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        return []

def display_result(results: List[Dict[str, str]]) -> None:
    """Displays the scan results in a formatted table."""
    if not results:
        logger.warning("No hosts found or scan failed.")
        return

    print("\n" + "="*40)
    print("IP Address\t\tMAC Address")
    print("="*40)
    for client in results:
        print(f"{client['ip']}\t\t{client['mac']}")
    print("="*40 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Network Scanner - Discover live hosts via ARP.")
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range (e.g. 192.168.1.1/24)")
    args = parser.parse_args()

    if not args.target:
        target = input("Enter target IP/Range (e.g. 192.168.1.0/24): ").strip()
    else:
        target = args.target

    if target:
        scan_result = scan_network(target)
        display_result(scan_result)

if __name__ == "__main__":
    main()
