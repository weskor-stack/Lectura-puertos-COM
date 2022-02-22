mensaje1 = 'hola mundo'
mensaje2 = "hola mundo"
mensaje3 = """Hola
hola
hola mundo"""

file = open('ejemplo.txt','a')
file.write("mensaje 1: " + mensaje1+"\n")
file.write("mensaje 2: " + mensaje2+"\n")
file.write("mensaje 3: " + mensaje3)

from datetime import datetime
now = datetime.now()
file.write(str(now))
print(now)