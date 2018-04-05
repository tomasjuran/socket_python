import socket

HOST = 'localhost'
PORT = 3500
RECBYTES = 1024

entrada = input("Ingrese un número\n")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(entrada.encode(), (HOST, PORT))
data, address = s.recvfrom(RECBYTES)
s.close()
print(data.decode())