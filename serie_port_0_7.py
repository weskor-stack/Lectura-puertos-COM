__author__ = "Edgar Bonilla Rivas"
__copyright__ = "Copyright (C) 2022 Author Name"
__license__ = "Public Domain"
__version__ = "1.0"

from asyncore import read
from ctypes.wintypes import PINT
from email import message
import socket
import sys
import serial
import time
import serial.tools.list_ports
from datetime import datetime
import gc


#file = open('data_plc.txt','a')
gc.collect()
encontrados = []
mensaje = ""
def puertos_encontrados():
    

    #Método para leer los puertos y almacenarlos en lista

    ports = ['COM%s' % (i + 2) for i in range(256)]

    for port in ports:
        try:

            s = serial.Serial(port)
            #print (s)
            s.close()
            encontrados.append(port)

        except (OSError, serial.SerialException):

            pass
        #mprime puertos encontrados
    print(encontrados, flush=True)
    return encontrados


def conexion():
    direccion_ip = socket.gethostbyname(socket.gethostname())
    #direccion_ip = "192.168.3.216"
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (direccion_ip, 10000)
    print('starting up on {} port {}'.format(*server_address), flush=True)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(2)
    puertos_encontrados()

    while True:
        # Wait for a connection
        print('waiting for a connection', flush=True)
        connection, client_address = sock.accept()
        try:
            data = connection.recv(1024)
            print('received {!r}'.format(data), flush=True)
            puerto_libre=0
            print('connection from', client_address, flush=True)
            # Receive the data in small chunks and retransmit it
            while True:
                try:
                    if data == b"":
                        print("no hay datos del ", client_address, flush=True)
                        break
                    else:
                        for puertos in encontrados:
                            puerto_libre = puertos
                            puerto   = serial.Serial(port = str(puerto_libre),
                                                    baudrate = 115200,
                                                    timeout= 0.5,
                                                    bytesize = serial.EIGHTBITS,
                                                    parity   = serial.PARITY_NONE,
                                                    stopbits = serial.STOPBITS_ONE)
                            print("Es el puerto: "+puerto_libre, flush=True)

                            try:
                                file = open('C:\DTA\data\data_plc.txt','a')
                                now = datetime.now()
                                if puerto.isOpen():
                                    print("El puerto %s está abierto! "% puerto_libre, flush=True)
                                    datos = str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                                    print("Los datos del puerto "+puerto_libre+" son: "+datos, flush=True)
                                    if datos !="":
                                        answer=""
                                        while  puerto.inWaiting()>0: #self.serial.readable() and
                                            
                                            #print(puerto.inWaiting(), flush=True)
                                            answer += "\n"+str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                                            #print(self.serial.inWaiting())
                                        #self.desc.setText(self.desc.toPlainText()+"\n"+answer)
                                        #return answer
                                        file.write('\n'+ str(now))
                                        file.write('\n'+'Datos del puerto: '+str(puerto_libre)+'\n')
                                        file.write(answer)
                                        file.write('\n')
                                        #print(answer)
                                        mensaje = answer
                                        print(mensaje, flush=True)
                                        connection.sendall(str(puerto_libre).encode(encoding='utf-8'))
                                        connection.sendall(mensaje.encode(encoding='utf-8'))
                            except IOError: # if port is already opened, close it and open it again and print message 
                                puerto.close() 
                                puerto.open() 
                                print ("port was already open, was closed and opened again!", flush=True)
                        message = "-"
                        connection.sendall(message.encode(encoding='utf-8'))
                except:
                    break
                    
        finally:
            # Clean up the connection
            connection.close()
            #break

conexion()