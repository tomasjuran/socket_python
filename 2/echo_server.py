import socket

host = 'localhost'
port = 3500
maxpedidos = 5
recbytes = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host,port))
s.listen(maxpedidos)

while True:
    client, address = s.accept()
    data = client.recv(recbytes)
    print('Conexión desde: %s:%i' % (address[0], address[1]))
    if data:
        client.send(data)
    client.close()