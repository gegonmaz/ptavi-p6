#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
# Cogeremos el  argumento del sistema, para obtener la IP y el puerto
InfoCliente = sys.argv[2].split('@')
Cliente = InfoCliente[0]

# Dirección IP del servidor.
PuertoIp = InfoCliente[1].split(':')
IPServidor = str(PuertoIp[0])
Metodo = sys.argv[1].upper()

try:
    PuertoServidor = int(PuertoIp[1])
except ValueError:
    print('Error en IP PUERTO')

# Dirección IP del servidor.
# SERVER = 'localhost'
# PORT = 6001
if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((IPServidor, PuertoServidor))
    # Linea que enviara el cliente al servidor
    respuesta = (Metodo + ' sip:' + IPServidor + " SIP/2.0\r\n")
    my_socket.send(bytes(respuesta, 'utf-8'))
    try:
        mensajeServidor = my_socket.recv(1024).decode('utf-8')
        print(mensajeServidor)
    except ConnectionRefusedError:
        sys.exit("No se puede conectar al servidor")
    if str(sys.argv[1]) == 'INVITE':
        nombreCliente = Cliente
        print('BIENVENIDO ' + nombreCliente)
        # Contenido que vamos a enviar
        LINE = 'INVITE' + ' sip:' + Cliente + '@' + IPServidor + ' SIP/2.0\r\n'

        print("Enviando: " + LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        # comprobaciones de metodos
        print(data.decode('utf-8'))
        Esperamos = mensajeServidor.split("\r\n\r\n")[0:-1]
        if Esperamos == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ring' +
                         'SIP/2.0 200 OK']:
            EnvioCliente = ('ACK' ' sip:' + IPServidor + " SIP/2.0\r\n")
            my_socket.send(bytes(EnvioCliente, 'utf-8'))
    if str(sys.argv[1]) == 'BYE':
        nombreCliente = Cliente
        # Contenido que vamos a enviar
        LINE = 'BYE' + ' sip:' + Cliente + '@' + IPServidor + ' SIP/2.0\r\n'
        print('HASTA PRONTO ' + nombreCliente)

        print("Enviando: " + LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        # comprobaciones de metodos
        print(data.decode('utf-8'))

        # Terminamos la conexion
        print('Recibido -- ', data.decode('utf-8'))
        print("Terminando socket...")
        # Cerramos todo
        my_socket.close()
        print("Fin.")
