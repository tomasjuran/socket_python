import sys
import re
import subprocess
from cryptography.fernet import Fernet
from connect import *
from pdu_fija import *

# Cliente y servidor necesitan tener la misma clave simétrica
# generada con el programa generar_key.py

HOST = 'localhost'
PORT = 2222
USER = 'root'
PASS = ' '
KEYPATH = 'secret.key'

def cliente():
	with open(KEYPATH, 'r') as f:
		key = f.read().encode()
	cipher = Fernet(key)

	with client(HOST, PORT) as sock:
		entrada = recibir(sock)
		print(entrada)
		while 'quit()' not in entrada:
			salida = cipher.encrypt(input().encode())
			enviar(sock, salida.decode())
			entrada = recibir(sock)
			print(entrada)



def servidor():
	with open(KEYPATH, 'r') as f:
		key = f.read().encode()
	cipher = Fernet(key)

	with server(HOST, PORT) as sock:
		autenticar(sock, cipher)
		entrada = (cipher.decrypt(recibir(sock).encode())).decode()
		while entrada != 'exit':
			comando = entrada.split()
			salida = subprocess.run(comando, stdout=subprocess.PIPE).stdout
			enviar(sock, salida.decode())
			entrada = (cipher.decrypt(recibir(sock).encode())).decode()

		enviar(sock, 'quit()')



def autenticar(sock, cipher):
	intentos = 1
	enviar(sock, 'Ingrese el usuario:')
	usuario = (cipher.decrypt(recibir(sock).encode())).decode()
	while usuario != USER and intentos < 3:
		enviar(sock, 'El usuario ingresado no es válido')
		intentos+=1
		usuario = (cipher.decrypt(recibir(sock).encode())).decode()

	if usuario != USER:
		enviar(sock, 'Demasiados intentos fallidos\nquit()')
		sock.close()
		sys.exit()

	intentos = 1
	enviar(sock, 'Ingrese la contraseña:')
	password = (cipher.decrypt(recibir(sock).encode())).decode()
	while password != PASS and intentos < 3:
		enviar(sock, 'La contraseña ingresada no es válida')
		intentos+=1
		password = (cipher.decrypt(recibir(sock).encode())).decode()

	if password != PASS:
		enviar(sock, 'Demasiados intentos fallidos\nquit()')
		sock.close()
		sys.exit()

	enviar(sock, 'Se ha logueado con éxito. "exit" para salir')
	return 0;




if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] in 'Ss':
			servidor()
	else:
		cliente()