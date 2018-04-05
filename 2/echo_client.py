import socket

host = 'localhost'
port = 3500
recbytes = 1024
mensaje = 'Hola Mundo!'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
s.sendall(mensaje.encode())

data = s.recv(recbytes)
s.close()

print(data.decode())