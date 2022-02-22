__author__ = "Edgar Bonilla Rivas"
__copyright__ = "Copyright (C) 2022 Author Name"
__license__ = "Public Domain"
__version__ = "1.0"

import socket
import sys
import serial
import time
import serial.tools.list_ports

from datetime import datetime

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

#file = open('data_plc.txt','w')

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
###############################################################################################################            
            #lista que se utiliza para almacenar los puertos encontrados
            encontrados = []

        #Método para leer los puertos y almacenarlos en lista

            ports = ['COM%s' % (i + 1) for i in range(256)]

            for port in ports:

                try:

                    s = serial.Serial(port)
                    #print (s)
                    s.close()

                    encontrados.append(port)

                except (OSError, serial.SerialException):

                    pass

            #mprime puertos encontrados

            print(encontrados)
            puerto_libre=0

            while 1:
                for puertos in encontrados:
                        puerto_libre = puertos

                        puerto   = serial.Serial(port = str(puerto_libre),
                                                baudrate = 115200,
                                                timeout= 3,
                                                bytesize = serial.EIGHTBITS,
                                                parity   = serial.PARITY_NONE,
                                                stopbits = serial.STOPBITS_ONE)
                        print("Es el puerto: "+puerto_libre)
                        
                        try:
                            file = open('C:\DTA\data\data_plc.txt','a')
                            now = datetime.now()
                            if puerto.isOpen():
                                print("El puerto %s está abierto! "% puerto_libre)
                                try:
                                    while 1: #Esta parte lee los datos del puerto
                                        datos = str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                                        print(now)
                                        print("Los datos del puerto "+puerto_libre+" son: "+datos)
                                        #file.write(str(now)+"\n"+"Los datos del puerto "+puerto_libre+" son: "+datos+"\n"+"\n")
                                        #Checa si un puerto está mandando información
                                        if datos != "":
                                            data_port = datos
                                            message = "Los datos del puerto ".encode(encoding='utf-8')+puerto_libre.encode(encoding='utf-8')+" son: ".encode(encoding='utf-8')+data_port.encode(encoding='utf-8')+'\n'.encode(encoding='utf-8')
                                            #data_port.encode(encoding='utf-8')+'\n'.encode(encoding='utf-8')
                                            connection.sendall(message)
                                            file.write(data_port.encode(encoding='utf-8'))
                                            break
                                        else:
                                            print("no se reciben los datos")
                                            data_port=" "
                                            break
                                    # Manda mensaje a cada puerto
                                    puerto.write(data_port.encode())
                                    #time.sleep(0.5)
                                    #puerto.write('b'.encode())
                                    #file.write(now+"\n"+"Los datos del puerto "+puerto_libre+" son: "+datos+"\n")
                                    puerto.close()
                                
                                except serial.SerialException:
                                    print('Port is not available') 
                                
                                except serial.portNotOpenError:
                                    print('Attempting to use a port that is not open')
                                    print('End of script')
                                    

                        except IOError: # if port is already opened, close it and open it again and print message 
                            puerto.close() 
                            puerto.open() 
                            print ("port was already open, was closed and opened again!") 
                #break

################################################################################################################

    finally:
        # Clean up the connection
        connection.close()
        #break