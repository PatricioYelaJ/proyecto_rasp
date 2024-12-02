import pigpio
import time

# Inicialización de la instancia de pigpio
pi = pigpio.pi()

# Función de inicialización para configurar los pines desde el código principal
def inicialitza_pins(rs, e, d4, d5, d6, d7, pausa):
    global RS, E, D4, D5, D6, D7, PAUSA
    RS, E, D4, D5, D6, D7, PAUSA = rs, e, d4, d5, d6, d7, pausa
    pi.set_mode(RS, pigpio.OUTPUT)
    pi.set_mode(E, pigpio.OUTPUT)
    pi.set_mode(D4, pigpio.OUTPUT)
    pi.set_mode(D5, pigpio.OUTPUT)
    pi.set_mode(D6, pigpio.OUTPUT)
    pi.set_mode(D7, pigpio.OUTPUT)

def char2bin(char):
    """Convierte un carácter en una representación binaria de 8 bits y la retorna como una tupla de enteros."""
    strink = bin(ord(char))[2:]
    strink = '0' * (8 - len(strink)) + strink  
    resultat = ''
    for bit in strink:
        resultat = bit + resultat  
    res = resultat[4:] + resultat[:4]
    tupla = tuple([int(element) for element in res])
    return tupla

def modecomandament(valor):
    """Configura el modo de comando del display, ajustando el pin RS según si se envía una instrucción (False) o datos (True)."""
    if valor == False:
        pi.write(RS, 1)  # Enviar instrucción
    else:
        pi.write(RS, 0)  # Enviar datos
    pi.write(E, 0)  

def escriu_a_fila_u():
    """Mueve el cursor al inicio de la primera fila del display."""
    modecomandament(True) 
    escriu4bits(0, 0, 0, 0)  
    escriu4bits(0, 0, 0, 0)
  
def escriu_a_fila_dos():
    """Mueve el cursor al inicio de la segunda fila del display."""
    modecomandament(True) 
    escriu4bits(0, 0, 1, 1)  
    escriu4bits(0, 0, 0, 0)

def escriu4bits(b1, b2, b3, b4):
    """Envía 4 bits al display a través de los pines D4-D7."""
    pi.write(D4, b1)
    pi.write(D5, b2)
    pi.write(D6, b3)
    pi.write(D7, b4)  
    time.sleep(PAUSA)
    pi.write(E, 1) 
    pi.write(E, 0)       
    time.sleep(PAUSA)

def esborra_la_pantalla():
    """Envia la instrucción para borrar todo el display."""
    modecomandament(True)
    time.sleep(PAUSA)
    escriu4bits(0, 0, 0, 0) 
    escriu4bits(1, 0, 0, 0) 

def envia_dades_al_display(dada):
    """Envía un carácter (en forma de tupla de 8 bits) al display para mostrarlo."""
    modecomandament(False) 
    escriu4bits(dada[0], dada[1], dada[2], dada[3]) 
    escriu4bits(dada[4], dada[5], dada[6], dada[7])

def detencio_pantalla():
    """Pone el display en modo de detención o pausa."""
    modecomandament(True) 
    escriu4bits(0, 0, 0, 0) 
    escriu4bits(0, 0, 1, 1) 
   
def inicia_pantalla():
    """Configura el display para iniciarlo, configurándolo con dos filas y borrándolo."""
    modecomandament(True)
    for index in range(3):
        escriu4bits(1, 1, 0, 0)
    for index in range(2):
        escriu4bits(0, 1, 0, 0)
    escriu4bits(1, 0, 1, 1)   
    escriu4bits(0, 0, 0, 0)
    escriu4bits(1, 1, 1, 1)
    esborra_la_pantalla()
