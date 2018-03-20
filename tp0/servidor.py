#!/usr/bin/env python3

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
	for i in input_string:
		temp = ord(i) - (shift % 26)
		if temp < ord('a'):
			decoded += chr(ord('z') + 1 + (temp % (- ord('a'))))
		else:
			decoded += chr(temp)

	return decoded


def recvall(socket, size):
	'''
		Receive all data of a certain size through a socket.

		@socket: Socket object to receive data through.
		@size: Total size of data to receive.

		@return: The complete data received.
	'''

	data = b''

	while len(data) < size:
		msg = socket.recv(size - len(data))

		if not msg:
			return None

		data += msg

	return data


def handle_client(con):
	'''
		Handle a new client connection.

		@con: Client socket.
	'''

	# Receive the string size from the client.
	msg = recvall(con, 4)
	string_size = struct.unpack('!i', msg)[0]

	# Receive the encoded string from the client.
	msg = recvall(con, string_size)
	encoded_string = msg.decode('ascii')

	# Receive the Caesar Cipher shift value from the client.
	msg = recvall(con, 4)
	caesar_shift = struct.unpack('!i', msg)[0]

	decoded = decode_caesar(encoded_string, caesar_shift)
	print(decoded)

	# Send decoded string back to client.
	con.sendall(decoded.encode('ascii'))


def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Set timeout for recv.
	rcv_timeo = struct.pack('ll', 15, 0)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, rcv_timeo)

	orig = ('', args.port_server)
	server.bind(orig)

	while True:
		server.listen(1)

		try:
			con, client = server.accept()
		except BlockingIOError:
			continue
			
		t = threading.Thread(target=handle_client, args=(con,))
		t.start()

	server.close()


main()