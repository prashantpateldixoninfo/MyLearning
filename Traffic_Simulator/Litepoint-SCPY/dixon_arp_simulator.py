from scapy.all import *


def send_arp_request():
    target_ip = "192.168.1.1"  # Replace with your gateway or target IP
    arp_request = ARP(pdst=target_ip)  # type: ignore
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")  # type: ignore
    arp_packet = broadcast / arp_request

    print(f"Sending ARP Request to {target_ip}")
    sendp(arp_packet, iface="Wi-Fi")  # Replace with your interface name


send_arp_request()
