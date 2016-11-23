#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    Metodos = ['INVITE', 'BYE', 'ACK']

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP_Cliente = str(self.client_address[0])
        PUERTO = int(self.client_address[1])
        audio = sys.argv[3]
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            # Partimos el mensaje
            Mensaje_Cliente = line.decode('utf-8').split()
            # Analizamos la linea para ver que metodo nos llega y contestar
            # Comprobamos el tamaño del paquete recibido
            if not line:
                break
            if Mensaje_Cliente[0] == 'INVITE':
                # INVITE --> tendremos que establecer la llamada(Comunicacion)
                envio = ("SIP/2.0 100 Trying\r\n\r\nSIP/2.0 180 Ring\r\n\r\n" +
                         "SIP/2.0 200 OK\r\n\r\n")
                self.wfile.write(bytes(envio, 'utf-8'))
            elif Mensaje_Cliente[0] == 'ACK':
                os.system("./mp32rtp -i " + IP_Cliente + " -p 23032 <" + audio)
            elif Mensaje_Cliente[0] == 'BYE':
                # BYE --> se cierra la comunicación
                envio = self.wfile.write(b'SIP/2.0 200 Ok\r\n\r\n')
            if not Mensaje_Cliente[0] in self.Metodos:
                # if not Mensaje_Cliente[0] == 'INVITE'|'BYE'|'ACK':
                envio = self.wfile.write((b'SIP/2.0 405 Method Not Allowed') +
                                         (b'\r\n\r\n'))
            else:
                envio = self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    # serv = socketserver.UDPServer(('', 6001), EchoHandler)
    # print("Lanzando servidor UDP de eco...")
    """
    Este es el programa para un servidor eco, pero ahora no queremos que el
    servidor conteste lo le envia el cliente. Queremos las respuestas propias.
    """
    # Primero comprobaremos el tamaño del mensaje que nos llega.
    if len(sys.argv) != 4:
        sys.exit("Usage: python server.py IP port audio_file")
    # Nos guardamos las variables de puerto y direccion IP del servidor
    try:
        IP_Servidor = sys.argv[1]
        PUERTO_Servidor = sys.argv[2]
        """
        Ademas ahora a parte del puerto y la direccion IP, encontramos
        el archivo de audio que enviamos por RTP
        """
        Archivo = sys.argv[3]
    except IndexError:
        sys.exit("Usage: python server.py IP port audio_file")
    # Creamos un servidor y escuchamos
    try:
        serv = socketserver.UDPServer(("", int(PUERTO_Servidor)), EchoHandler)
    except ValueError:
        sys.exit('El Puerto necesita un entero')

    print("Estamos escuchando en el puerto " + PUERTO_Servidor)
    serv.serve_forever()
