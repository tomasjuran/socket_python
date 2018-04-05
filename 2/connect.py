import socket

def client(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print('Conectado a %s:%i' % (host, port))
	return s

def server(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
	s.listen(1)
	print('Servidor escuchando en %s:%i' % (host, port))
	c, address = s.accept()
	print('Conexión desde %s:%i' % (address[0], address[1]))
	return c