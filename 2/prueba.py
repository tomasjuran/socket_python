import re
from http_client import *

url = 'https://www.example.com/sub/hola/index.html'

(host, port, recurso) = procesar_entrada(url, '')


header = '\
Content-Length: 2008\r\n\
Location: http://www.example.com/index.html\r\n'

dic = {}

for (field, value) in re.findall(r'(.+): (.+)', header):
	dic[field] = value

with open('archivo.txt', 'w') as f:
	for key, value in dic.items():
		f.write(key + ': ' + value + '\r\n')