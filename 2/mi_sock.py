import socket

def mi_send(sock, msg):
	totalsent = 0
	while totalsent < len(msg):
		sent = sock.send(msg[totalsent:])
		if sent == 0:
			raise RuntimeError("Socket connection broken")
		totalsent = totalsent + sent

def mi_recv(sock, recbytes):
	msg = sock.recv(recbytes)
	if msg == b'':
		raise RuntimeError("Socket connection broken")
	return msg