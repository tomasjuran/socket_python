from mi_sock import *

# PDU de aplicación de longitud variable
# determinada por tokens

recbytes = 2048
token = ' '

def enviar(sock):
	mensaje = input()
	pos = mensaje.find(token)
	while pos > -1:
		pos += 1
		chunk = mensaje[:pos]
		mi_send(sock, chunk.encode())
		mensaje = mensaje[pos:]
		pos = mensaje.find(token)
	mi_send(sock, mensaje.encode())

def recibir(sock):
	mensaje = mi_recv(sock, recbytes)
	mensaje = mensaje.decode()
	i = 1
	pos = mensaje.find(token)
	while pos > -1:
		pos += 1
		chunk = mensaje[:pos]
		print('#%i: %s' % (i, chunk))
		mensaje = mensaje[pos:]
		# Si el mensaje termina en un token queda más por recuperar
		if mensaje == '':
			mensaje = mi_recv(sock, recbytes)
			mensaje = mensaje.decode()	
		i += 1
		pos = mensaje.find(token)
	print('#%i: %s' % (i, mensaje))