#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP_Cliente = str(self.client_address[0])
        PUERTO = int(self.client_address[1])
        print('El cliente está escuchando en dirección ' + IP_CLiente + ' y puerto ' 
                + PUERTO)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            # Partimos el mensaje
            Mensaje_Cliente = line.decode('utf-8').split()
            # Analizamos la linea para ver que metodo nos llega y contestar 
            if Mensaje_Cliente[0] == 'INVITE':
            # INVITE --> tendremos que establecer la llamada(Comunicacion)                
                self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n')
                self.wfile.write(b'SIP/2.0 180 Ring\r\n\r\n')
                self.wfile.write(b'SIP/2.0 200 Ok\r\n\r\n')
            elif argv[0] == 'BYE':
            # BYE --> se cierra la comunicación
                self.wfile.write(b'SIP/2.0 200 Ok\r\n\r\n')
            elif argv[0] == 'ACK':

            if not argv[0] == 'INVITE'|'BYE':
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n') 
            else:
                self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

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
    serv = socketserver.UDPServer(("", int(PUERTO_Servidor)), EcoHandler)
    print("Estamos escuchando en el puerto " +  PUERTO)
    serv.serve_forever()
