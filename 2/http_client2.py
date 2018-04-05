import sys
import socket
from mi_sock import *

# El programa recibe como argumentos la dirección y el nombre del recurso
# ejemplo:
# $ python3 http_client.py 192.168.0.1 index.html

http_port = 80
charset = 'iso-8859-1'

def conectar(host):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, http_port))
	print('Conectado a: %s:%i' % (host, http_port))
	return s

def requerir(direccion, recurso):
	sock = conectar(direccion)
	mensaje = '\
GET ' + recurso + ' HTTP/1.1\r\n\
Host: a\r\n\
Accept: text/html\r\n\
Accept-Encoding: deflate\r\n\r\n'
	mi_send(sock, mensaje.encode())

	header = mi_recv(sock, 1024)
	
	while header.find(b'Content-Length:') < 0:
		header += mi_recv(sock, 1024)
	ini = header.find(b'Content-Length:') + 16
	
	while header[ini:].find(b'\r\n') < 0:
		header += mi_recv(sock, 1024)
	fin = header[ini:].find(b'\r\n') + ini
	
	body_size = int(header[ini:fin].decode(charset))
	body = header[header.find(b'\r\n\r\n'):]
	while len(body) < body_size:
		body += mi_recv(sock, 1024)

	print(body.decode(charset))

if __name__ == '__main__':
	if len(sys.argv) > 2:
		direccion = sys.argv[1]
		recurso = sys.argv[2]
		requerir(direccion, recurso)