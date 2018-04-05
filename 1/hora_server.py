import socket
from datetime import datetime, timedelta

host = 'localhost'
port = 3500
recbytes = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

while True:
    data, address = s.recvfrom(recbytes)
    print('Conexión desde: %s:%i' % (address[0], address[1]))
    if data.decode():
    	zona = data.decode()
    	huso = timedelta(hours = 3 + int(zona))
    else:
    	zona = '-3' # hora del servidor
    	huso = timedelta()
    # datetime.datetime.now() es la hora actual
    now = datetime.now() + huso
    # eliminar microsegundos
    now = now.replace(microsecond = 0)
    respuesta = str(now) + ' UTC ' + zona
    print(respuesta)
    s.sendto(respuesta.encode(), address)