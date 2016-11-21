#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
# Cogeremos el  argumento del sistema, para obtener la IP y el puerto
InfoCliente = sys.argv[3].split('@')
Cliente = InfoCliente[0]

# Dirección IP del servidor.
PuertoIp = InfoCliente[1].split(':')
IPServidor = str(PuertoIp[0])

try:
    PuertoServidor = int(PuertoIp[1])
except ValueError:
    print('Error en IP PUERTO')

# Dirección IP del servidor.
# SERVER = 'localhost'
# PORT = 6001

if str(sys.argv[1]) == 'INVITE':
    nombreCliente = Cliente
    print('BIENVENIDO ' + nombreCliente)
    # Contenido que vamos a enviar
    LINE = 'INVITE' + ' sip:' + Cliente + '@' + IPServidor + ' SIP/2.0\r\n'

if str(sys.argv[1] == 'BYE':
    nombreCliente = Cliente
    # Contenido que vamos a enviar
    LINE = 'BYE' + ' sip:' + Cliente + '@' + IPServidor + ' SIP/2.0\r\n'
    print('HASTA PRONTO ' + nombreCliente)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)


print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
