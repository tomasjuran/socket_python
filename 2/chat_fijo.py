from mi_sock import *

# PDU de aplicación de longitud fija
# Contiene solo datos

msglen = 1024

def enviar(sock):
	mensaje = input()
	while len(mensaje) > msglen:
		mi_send(sock, mensaje[:msglen].encode())
		mensaje = mensaje[msglen:]
	mensaje = mensaje.ljust(msglen, '\0')
	mi_send(sock, mensaje.encode())

def recibir(sock):
	mensaje = ''
	while len(mensaje) < msglen:
		mensaje += mi_recv(sock, msglen).decode()
	print(mensaje)