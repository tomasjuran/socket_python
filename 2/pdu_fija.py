from mi_sock import *

MSGLEN = 2048

def enviar(sock, mensaje, msglen = MSGLEN):
	while len(mensaje) > msglen:
		mi_send(sock, mensaje[:msglen].encode())
		mensaje = mensaje[msglen:]
	mensaje = mensaje.ljust(msglen, '\0')
	mi_send(sock, mensaje.encode())

def recibir(sock, msglen = MSGLEN):
	mensaje = ''
	while len(mensaje) < msglen:
		mensaje += mi_recv(sock, msglen).decode()
	return mensaje