#!/usr/bin/env python2

'''
Trabalho Pratico 0: Redes de Computadores DCC023
Autor: Hugo Araujo de Sousa (2013007463)
cliente.py: Sends a string to the server and gets it back encrypted.
'''

import argparse as ap
import socket
import struct

# Add command line arguments.
parser = ap.ArgumentParser()

parser.add_argument('ip_server', type=str, help='Server IP address')
parser.add_argument('port_server', type=int, help='Server port')
parser.add_argument('input_string', type=str, help='Input string to encrypt')
parser.add_argument('shift', type=int, \
	help='Unsigned integer to use in Caesar Cipher')

args = parser.parse_args()


def caesar_cipher(input_string, shift):
	'''
		Applies the Caesar Cipher to a string.

		@input_string:	String to encode.
		@shift: Unsigned integer that represents the number of shifts to apply
			to each character.

		@return: String that represents the input string after Caesar Cipher 
			encoding.
	'''

	encoded = ''
	for i in input_string: encoded = encoded + chr(ord(i) + shift)
	return encoded


def main():
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (args.ip_server, args.port_server)
	tcp.connect(dest)

	input_string_size = len(args.input_string)
	
	# Send size of input string to server.
	msg = struct.pack('!i', input_string_size)
	tcp.send(msg)

	# Send the encoded string to server.
	msg = caesar_cipher(args.input_string, args.shift)
	tcp.send(msg)

	# Send the Caesar Cipher shift to server.
	msg = struct.pack('!i', args.shift)
	tcp.send(msg)

	# Receive string from server.
	server_string = tcp.recv(input_string_size)

	print 'Received \'' + server_string + '\' from server.'
	tcp.close()


main()