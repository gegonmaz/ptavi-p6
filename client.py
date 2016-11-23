#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

try:
    # Cogeremos el  argumento del sistema, para obtener la IP y el puerto
    InfoCliente = sys.argv[2].split('@')
    Cliente = InfoCliente[0]

    # Dirección IP del servidor.
    PuertoIp = InfoCliente[1].split(':')
    IPServidor = str(PuertoIp[0])
    Metodo = sys.argv[1].upper()
    PuertoServidor = int(PuertoIp[1])
except ValueError:
    print('Error en IP PUERTO')

# Dirección IP del servidor.
# SERVER = 'localhost'
# PORT = 6001
if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IPServidor, PuertoServidor))
# Linea que enviara el cliente al servidor
LINE = (Metodo + ' sip:' + IPServidor + " SIP/2.0")
print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
# Ahora recibiremos el mensaje del servidor
mensajeServidor = my_socket.recv(1024).decode('utf-8')
print('El servidor manda: ' + mensajeServidor)
Respuesta = mensajeServidor.split()
if Respuesta[1] == '100' and Respuesta[4] == '180' and Respuesta[7] == '200':
    EnvioCliente = ('ACK' + ' sip:' + IPServidor + " SIP/2.0\r\n")
    my_socket.send(bytes(EnvioCliente, 'utf-8'))
try:
    data = my_socket.recv(1024)
except ConnectionRefusedError:
    sys.exit(" Connection Refused ERROR ")

print('Recibido -- ', data.decode('utf-8'))
# Terminamos la conexion
print("Terminando socket...")
# Cerramos todo
my_socket.close()
print("Fin.")
