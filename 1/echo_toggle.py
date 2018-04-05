import sys
import socket

host = 'localhost'
port = 3500
recbytes = 1024

def server():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))

	while True:
	    data, address = s.recvfrom(recbytes)
	    print('Conexion desde: %s:%i' % (address[0], address[1]))
	    if data:
	        s.sendto(data, address)

def client():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	mensaje = 'Taller II: Echo sobre UDP' 
	s.sendto(mensaje.encode(), (host, port))
	data, address = s.recvfrom(recbytes)
	s.close()
	print('-->', data.decode())

if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == 's':
			server()
	else:
		client()
