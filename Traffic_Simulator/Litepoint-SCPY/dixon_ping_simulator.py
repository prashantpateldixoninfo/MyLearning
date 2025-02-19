from scapy.all import *


def send_icmp_request():
    target_ip = "8.8.8.8"  # Replace with your target IP
    icmp_request = IP(dst=target_ip) / ICMP()  # type: ignore

    print(f"Pinging {target_ip}")
    response = sr1(icmp_request, timeout=2)

    if response:
        print(f"Received reply from {target_ip}: {response.summary()}")
    else:
        print("No reply received.")


send_icmp_request()
