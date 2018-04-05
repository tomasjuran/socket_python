import sys
import socket
import re
from urllib.parse import urlparse
from datetime import datetime
from mi_sock import *

# El programa recibe como argumento la url completa
# ejemplo:
# $ python3 http_client.py http://192.168.0.1/index.html
#
# Para utilizar un proxy, agregue "via" <direccion proxy> al final
# ejemplo:
# $ python3 http_client.py http://192.168.0.1/index.html via 10.0.0.1:8080

HTTP_PORT = 80
HTTPS_PORT = 443
CHARSET = 'iso-8859-1'
RECBYTES = 1024
LOG_FILE = 'headers.log'

def conectar(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print('Conectado a: %s:%i' % (host, port))
	return s

def requerir(url, proxy = ''):

	host, port, recurso = procesar_entrada(url, proxy)

	mensaje = armar_mensaje(host, recurso)

	with conectar(host, port) as sock:
		mi_send(sock, mensaje.encode())

		received = ''
		# Recuperar todo el header
		while received.find('\r\n\r\n') < 0:
			received += mi_recv(sock, RECBYTES).decode(CHARSET)
		
		header, body = received.split('\r\n\r\n', 1)

		log_header(mensaje, header)

		dict_header = procesar_header(header)

		# Si se está redireccionando
		status_line = header.split('\r\n', 1)[0]
		[status_code] = re.findall('\d{3}', status_line)
		if int(status_code) in range(300, 399):
			redir_url = dict_header.get('Location', None)
			if redir_url:
				print('Redirección a ' + redir_url)
				requerir(redir_url, proxy)
				return 0
			else:
				error = ('Se encontró la línea de estado\n'
						 + status_line + '\ny se intentó una redirección,'
						 + ' pero el header no contenía el campo "Location"')
				raise Exception(error)


		# Si queda payload por recuperar
		cont_len = dict_header.get('Content-Length', None)
		if cont_len:
			cont_len = int(cont_len)
			while len(body) < cont_len:
				body += mi_recv(sock, RECBYTES).decode(CHARSET)		



		print(body)



def procesar_entrada(url, proxy):
	"""Devuelve el host, puerto y recurso extraídos de la url y el proxy"""
	if proxy:
		[(host, port)] = re.findall(r'(.+?):(\d+)', proxy)
		port = int(port)
		recurso = url
	else:
		if not re.match(r'^https?://', url):
			url = 'http://' + url
		
		urlp = urlparse(url)

		host = urlp.netloc
		if urlp.scheme == 'https':
			port = HTTPS_PORT
		else:
			port = HTTP_PORT
		
		recurso = urlp.path
		if not recurso:
			recurso = '/'


	return host, port, recurso



def armar_mensaje(host, recurso):
	"""Arma el header de la solicitud HTTP"""
	mensaje = '\
GET ' + recurso + ' HTTP/1.1\r\n\
Host: ' + host + '\r\n\r\n'
	return mensaje



def procesar_header(header):
	"""Devuelve un diccionario con campo:valor para cada campo del header"""
	dict_header = {}
	for (field, value) in re.findall(r'(.+): (.+)\r\n', header):
		dict_header[field] = value
	return dict_header


def log_header(mensaje, header):
	"""Almacena los headers recibidos en un archivo de log"""
	with open(LOG_FILE, 'a') as log:
		log.write('[' + str(datetime.now()) + ']\r\n')
		log.write('[Solicitud]\r\n')
		log.write(mensaje)
		log.write('[Respuesta]\r\n')
		log.write(header + '\r\n\r\n')
		log.write('----------------------------------------\r\n\r\n')


if __name__ == '__main__':
	if len(sys.argv) > 1:
		if len(sys.argv) > 3:
			requerir(sys.argv[1], sys.argv[3])
		else:
			requerir(sys.argv[1])