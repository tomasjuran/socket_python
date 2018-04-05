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
	mi_send(sock, (mensaje + token).encode())

def recibir(sock):
	pos = -1
	mensaje = ''
	i = 1
	
	# Recibir hasta encontrar un token
	while pos <= -1:
		chunk = mi_recv(sock, recbytes)
		chunk = chunk.decode()
		mensaje += chunk
		pos = mensaje.find(token)
		
		# Mostrar todos los mensajes recuperados
		while pos > -1:
			pos += 1
			chunk = mensaje[:pos]
			print('#%i: %s' % (i, chunk))
			i += 1
			mensaje = mensaje[pos:]
			pos = mensaje.find(token)
			
		# Si se sale del while anterior con algo en mensaje, se trata de un
		# mensaje incompleto. Como pos == -1, se vuelve a recibir hasta
		# encontrar un token. De lo contrario (ya no quedan mensajes), salir
		if mensaje == '':
			break