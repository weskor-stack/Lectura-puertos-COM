__author__ = "Edgar Bonilla Rivas"
__copyright__ = "Copyright (C) 2022 Author Name"
__license__ = "Public Domain"
__version__ = "1.0"

from asyncio.windows_events import NULL
from asyncore import read
from email import message
import socket
import sys
import serial
import time
import serial.tools.list_ports


def conexion():
    direccion_ip = socket.gethostbyname(socket.gethostname())
    #direccion_ip = "192.168.3.216"
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (direccion_ip, 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            data = connection.recv(1024)
            print('received {!r}'.format(data))
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:
                try:
                    if data == b"":
                        print("no hay datos del ", client_address)
                        break
                    else:
                        print('Enviando datos')
                        message = "Envio de datos"
                        connection.sendall(message.encode(encoding='utf-8'))
                except:
                    break
                    
        finally:
            # Clean up the connection
            connection.close()
            #break

conexion()