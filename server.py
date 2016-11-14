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
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            # Analizamos la direccion IP y el PUERTO
            IP = str(self.client_address[0])
            print('Dir. IP del cliente: ' + IP)
            PUERTO = str(self.client_address[1])
            print('Puerto donde escucha cliente: ' + PUERTO)
            # Analizamos la linea para ver que metodo nos llega y contestar 
            if argv[2] == 'INVITE':
            # INVITE --> tendremos que establecer la llamada(Comunicacion)                
                self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n')
                self.wfile.write(b'SIP/2.0 180 Ring\r\n\r\n')
                self.wfile.write(b'SIP/2.0 200 Ok\r\n\r\n')
            if argv[2] == 'BYE':
            # BYE --> se cierra la comunicación
                self.wfile.write(b'SIP/2.0 200 Ok\r\n\r\n')
            if not argv[2] == 'INVITE'|'BYE':
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n') 
            else:
                self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', 6001), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
