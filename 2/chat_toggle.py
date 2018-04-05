import os
import sys
import socket
#from chat_fijo import *
from chat_token import *
#from chat_var import *

host = 'localhost'
port = 3500

def run(sock):
	pid = os.fork()
	if pid == 0: # Hijo
		while True:
			enviar(sock)
	else: # Padre
		while True:
			recibir(sock)


def server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
	s.listen(1)
	c, address = s.accept()
	print('Conexión desde: %s:%i' % (address[0], address[1]))
	run(c)

def client():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print('Conectado a: %s:%i' % (host, port))
	run(s)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == 's':
			server()
	else:
		client()