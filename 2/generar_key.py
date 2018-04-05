from cryptography.fernet import Fernet

# Genera una key simétrica con el módulo cryptography.fernet
# para ser usada por pseudo_ssh

FILENAME = 'secret.key'

with open(FILENAME, 'w') as f:
	f.write(Fernet.generate_key().decode())

print('La key se generó en el archivo ' + FILENAME)