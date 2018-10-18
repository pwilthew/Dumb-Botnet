"""Service script to wait and obtain bots' IPs.

This script should be run as a service. Its goal
is to maintain a list of the bots' IP addresses
that have reached out so far.
"""

import ipaddress
from pwn import *

BOTS_IPS = 'bots_ips.txt'
LPORT = 11111


def main():
    """Write bots' IP addresses to the BOTS_IPS file.

    Wait for bots to connect and send their IP addresses,
    then write them to the file.
    """
    while True:
        # Wait for a bot to connect.
        l = listen(LPORT)
        _ = l.wait_for_connection()

        # Ask for its IP address.
        l.sendline('Hi, what\'s your IP?')
        ip = l.recvline().strip('\n')

        if not is_ip_valid(ip):
            continue

        # Get the current bots' IP addresses from the file
        # and store them in a set.
        with open(BOTS_IPS, 'r') as bots_file:
            set_of_bots_ips = set(x for x in bots_file.readlines())

        # Add the new bot IP address to the set.
        set_of_bots_ips.add(ip)

        # Overwrite the file with the new set to avoid
        # duplicate IP addresses.
        with open(BOTS_IPS, 'w') as bots_file:
            bots_file.write('\n'.join(set_of_bots_ips))


def is_ip_valid(ip):
    """Determine if a string `ip` is a valid IP.

    Args:
        ip (str): A possible IP address.

    Returns:
        bool: True is `ip` is a valid IP address.
    """
    try:
        ipaddress.ip_address(unicode(ip))
    except:
        return False
    return True


if __name__ == '__main__':
    main()