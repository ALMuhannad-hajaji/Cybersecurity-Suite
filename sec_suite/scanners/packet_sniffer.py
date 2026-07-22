import sys
import argparse
import scapy.all as scapy
from sec_suite.utils.logger import get_logger

logger = get_logger(__name__)
packet_count = 0
limit = 0

def process_packet(packet):
    """Callback function to process and display packet details."""
    global packet_count, limit
    
    if limit > 0 and packet_count >= limit:
        return False  # Stops sniffing

    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        protocol = packet[scapy.IP].proto
        
        proto_name = "TCP" if protocol == 6 else "UDP" if protocol == 17 else "ICMP" if protocol == 1 else str(protocol)
        
        packet_count += 1
        print(f"[{packet_count}] {proto_name} Packet: {src_ip} -> {dst_ip}")

def start_sniffing(interface: str = None, packet_limit: int = 0):
    """Starts the Scapy packet sniffer."""
    global limit, packet_count
    limit = packet_limit
    packet_count = 0
    
    logger.info(f"Starting packet sniffer... (Limit: {limit if limit > 0 else 'Unlimited'})")
    try:
        if interface:
            scapy.sniff(iface=interface, store=False, prn=process_packet)
        else:
            scapy.sniff(store=False, prn=process_packet)
    except PermissionError:
        logger.error("Permission denied. Packet sniffing requires root/administrator privileges.")
    except Exception as e:
        logger.error(f"Sniffer error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Packet Sniffer using Scapy")
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to sniff on (e.g. eth0, wlan0)")
    parser.add_argument("-c", "--count", dest="count", type=int, help="Number of packets to capture", default=0)
    
    args = parser.parse_args()
    
    if not sys.argv[1:]:
        interface = input("Enter interface (leave blank for default): ").strip() or None
        count_input = input("Enter packet limit (0 for unlimited): ").strip()
        count = int(count_input) if count_input.isdigit() else 0
    else:
        interface = args.interface
        count = args.count

    try:
        start_sniffing(interface, count)
    except KeyboardInterrupt:
        logger.info("\nSniffing stopped by user.")

if __name__ == "__main__":
    main()
