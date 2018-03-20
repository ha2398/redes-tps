#!/usr/bin/env python3

'''
Trabalho Pratico 0: Redes de Computadores DCC023
Autor: Hugo Araujo de Sousa (2013007463)
cliente.py: Sends an encoded string to the server and gets it back decoded.
'''

import argparse as ap
import socket
import struct

# Add command line arguments.
parser = ap.ArgumentParser()

parser.add_argument('ip_server', type=str, help='Server IP address')
parser.add_argument('port_server', type=int, help='Server port')
parser.add_argument('input_string', type=str, help='Input string to decode')
parser.add_argument('shift', type=int, \
	help='Unsigned integer to use in Caesar Cipher')

args = parser.parse_args()


def caesar_cipher(input_string, shift):
	'''
		Apply the Caesar Cipher to a string.

		@input_string:	String to encode.
		@shift: Unsigned integer that represents the number of shifts to apply
			to each character.

		@return: String that represents the input string after Caesar Cipher 
			encoding.
	'''

	encoded = ''
	for i in input_string:
		temp = ord(i) + shift % 26
		if temp > ord('z'):
			encoded += chr((temp % (ord('z') + 1)) + ord('a'))
		else:
			encoded += chr(temp)

	return encoded


def main():
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Set timeout for recv.
	rcv_timeo = struct.pack('ll', 15, 0)
	tcp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, rcv_timeo)

	dest = (args.ip_server, args.port_server)
	tcp.connect(dest)

	input_string_size = len(args.input_string)
	
	# Send size of input string to server.
	msg = struct.pack('!i', input_string_size)
	tcp.send(msg)

	# Send the encoded string to server.
	msg = caesar_cipher(args.input_string, args.shift)
	tcp.send(msg.encode('ascii'))

	# Send the Caesar Cipher shift to server.
	msg = struct.pack('!i', args.shift)
	tcp.send(msg)

	# Receive string from server.
	server_string = tcp.recv(input_string_size)

	print(server_string.decode('ascii'))
	tcp.close()


main()