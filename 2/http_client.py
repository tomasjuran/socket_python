import sys
import socket
from mi_sock import *

# El programa recibe como argumentos la dirección y el nombre del recurso
# ejemplo:
# $ python3 http_client.py 192.168.0.1 index.html

http_port = 80
charset = 'iso-8859-1'
recbytes = 1024

def conectar(host):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, http_port))
	print('Conectado a: %s:%i' % (host, http_port))
	return s

def requerir(direccion, recurso):
	sock = conectar(direccion)
	mensaje = '\
GET ' + recurso + ' HTTP/1.1\r\n\
Host: ' + direccion + '\r\n\
Accept: text/html\r\n\r\n'

	mi_send(sock, mensaje.encode())

	resp = mi_recv(sock, recbytes)
	
	while resp.find(b'</html>') == -1:
		resp += mi_recv(sock, recbytes)
	
	head_end = resp.find(b'\r\n\r\n')
	header = resp[:head_end].decode(charset)
	body = resp[head_end:].decode(charset)

	print(header + '\n\n\nfin header')
	print(body)

if __name__ == '__main__':
	if len(sys.argv) > 2:
		direccion = sys.argv[1]
		recurso = sys.argv[2]
		requerir(direccion, recurso)