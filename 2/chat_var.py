from mi_sock import *
import datetime
import random
import zlib

# PDU aplicación con longitud variable y headers fijos

# Para la conversión de enteros
orden = 'big'

# Longitud del mensaje: entero sin signo 2 bytes
lendata = 2

# Campo ID: entero sin signo 2 bytes
lenid = 2
posid = lendata

# Campo Timestamp: string 32 bytes
lentime = 32
postime = posid + lenid

# Campo CRC: entero sin signo 4 bytes
lencrc = 4
poscrc = postime + lentime

# Tamaño total del header
h_size = lendata + lenid + lentime + lencrc

# Rutina interna para recuperar un número fijo de bytes
def recuperar(sock, msglen):
	recbytes = 0
	msg = b''
	while recbytes < msglen:
		msg += mi_recv(sock, msglen - recbytes)
		recbytes = len(msg)
	return msg

def enviar(sock):
	mensaje = input().encode()
	
	msglen = len(mensaje).to_bytes(lendata, orden)
	#print(str(int.from_bytes(msglen, orden)))
	
	msgid = random.randint(1,65535).to_bytes(lenid, orden)
	#print(str(int.from_bytes(msgid, orden)))

	timestamp = str(datetime.datetime.now())
	timestamp = timestamp.ljust(lentime).encode()
	#print(timestamp.decode())

	crc = zlib.crc32(mensaje).to_bytes(lencrc, orden)
	#print(str(int.from_bytes(crc, orden)))

	header = msglen + msgid + timestamp + crc
	mensaje = header + mensaje
	mi_send(sock, mensaje)

def recibir(sock):
	header = recuperar(sock, h_size)
	
	msglen = int.from_bytes(header[:lendata], byteorder=orden)
	msgid = int.from_bytes(header[posid:posid+lenid], byteorder=orden)
	timestamp = header[postime:postime+lentime].decode()
	crc = int.from_bytes(header[poscrc:poscrc+lencrc], byteorder=orden)
	
	#print('msglen: ' + str(msglen))
	print('id: ' + str(msgid))
	print('timestamp: ' + timestamp)
	#print('crc: ' + str(crc))

	mensaje = recuperar(sock, msglen)
	
	#if random.randint(0,1):
	#	mensaje = mensaje.decode() + "--modificación"
	#	mensaje = mensaje.encode()

	if crc != zlib.crc32(mensaje):
		print('¡El mensaje fue modificado!')
	
	print(mensaje.decode())