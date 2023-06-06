from scapy import *

packet = ARP(op=1, pdst="192.168.0.108")
