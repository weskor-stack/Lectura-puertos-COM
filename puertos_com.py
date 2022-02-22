
from email import message
from multiprocessing.connection import answer_challenge
import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports
import socket



file = open('data_plc.txt','a')
encontrados = []
mensaje = ""
def puertos_encontrados():
    

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
    return encontrados

def conexiones():
    puertos_encontrados()
    puerto_libre=0

    for puertos in encontrados:
        puerto_libre = puertos
        puerto   = serial.Serial(port = str(puerto_libre),
                                baudrate = 115200,
                                timeout= 5,
                                bytesize = serial.EIGHTBITS,
                                parity   = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE)
        print("Es el puerto: "+puerto_libre)

        try:
            if puerto.isOpen():
                print("El puerto %s está abierto! "% puerto_libre)
                datos = str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                print("Los datos del puerto "+puerto_libre+" son: "+datos)
                answer=""
                while  puerto.inWaiting()>0: #self.serial.readable() and
                    
                    print(puerto.inWaiting())
                    answer += "\n"+str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                    #print(self.serial.inWaiting())
                #self.desc.setText(self.desc.toPlainText()+"\n"+answer)
                #return answer
                file.write('\n'+'Datos del puerto: '+str(puerto_libre)+'\n')
                file.write(answer)
                file.write('\n')
                #print(answer)
                mensaje = answer
                print(mensaje)
        except IOError: # if port is already opened, close it and open it again and print message 
            puerto.close() 
            puerto.open() 
            print ("port was already open, was closed and opened again!")



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
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            print("Hola")
            print(mensaje)
            #conexiones()
            #mensaje = conexiones()
            connection.sendall(mensaje.encode(encoding='utf-8'))
        finally:
            # Clean up the connection
            connection.close()
            #break
#conexion()
conexiones()
