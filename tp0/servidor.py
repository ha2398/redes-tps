#!/usr/bin/env python2

'''
Trabalho Pratico 0: Redes de Computadores DCC023
Autor: Hugo Araujo de Sousa (2013007463)
servidor.py: Receives a string from each client, decodes it and sends it back
to client.
'''

import argparse as ap
import socket
import struct
import threading

# Add command line arguments.
parser = ap.ArgumentParser()
parser.add_argument('port_server', type=int, help='Server port')
args = parser.parse_args()


def decode_caesar(input_string, shift):
	'''
		Decodes a string encrypted with the Caesar Cipher.

		@input_string:	String to decode.
		@shift: Unsigned integer that represents the number of shifts applied to
			each character.

		@return: String that represents the input string after Caesar Cipher 
			decoding.
	'''

	decoded = ''
	for i in input_string: decoded = decoded + chr(ord(i) + shift)
	return decoded


def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Set timeout for recv.
	rcv_timeo = struct.pack('ll', 15, 0)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, rcv_timeo)

	orig = ('', args.port_server)
	server.bind(orig)
	server.listen(1)
	con, client = server.accept()

	# Receive the string size from the client.
	msg = con.recv(4)
	string_size = struct.unpack('!i', msg)[0]

	# Receive the encoded string from the client.
	encoded_string = con.recv(string_size)

	# Receive the Caesar Cipher shift value from the client.
	msg = con.recv(4)
	caesar_shift = struct.unpack('!i', msg)[0]

	decoded = decode_caesar(encoded_string, caesar_shift)
	print decoded

	# Send decoded string back to client.
	con.send(decoded)
	server.close()


main()