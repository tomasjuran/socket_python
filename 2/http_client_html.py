import sys
import socket
from mi_sock import *

# El programa recibe como argumentos la dirección y el nombre del recurso
# ejemplo:
# $ python3 http_client.py 192.168.0.1 /index.html
#
# Para utilizar un proxy, agregue "via" <direccion proxy> al final
# ejemplo:
# $ python3 http_client.py 192.168.0.1 /index.html via 10.0.0.1

HTTP_PORT = 80
CHARSET = 'iso-8859-1'
RECBYTES = 1024

def conectar(host):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, HTTP_PORT))
	print('Conectado a: %s:%i' % (host, HTTP_PORT))
	return s

def requerir(direccion, recurso, proxy = ''):
	if proxy:
		sock = conectar(proxy)
	else:
		sock = conectar(direccion)

	mensaje = '\
GET ' + recurso + ' HTTP/1.1\r\n\
Host: ' + direccion + '\r\n\
Accept: text/html\r\n\r\n'

	mi_send(sock, mensaje.encode())

	resp = mi_recv(sock, RECBYTES)
	
	while resp.find(b'</html>') == -1:
		resp += mi_recv(sock, RECBYTES)
	
	head_end = resp.find(b'\r\n\r\n')
	header = resp[:head_end].decode(CHARSET)
	body = resp[head_end:].decode(CHARSET)

	print(header + '\n\n\nfin header')
	print('\n' + body)



if __name__ == '__main__':
	if len(sys.argv) > 2:
		direccion = sys.argv[1]
		recurso = sys.argv[2]
		if len(sys.argv) > 4:
			requerir(direccion, recurso, sys.argv[4])
		else:
			requerir(direccion, recurso)