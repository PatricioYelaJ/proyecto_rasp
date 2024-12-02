import pigpio
import time

# Función de inicialización para establecer los valores de los pines desde el código principal
def inicialitza_pins(rs, e, d4, d5, d6, d7, pausa, pi):
    global RS, E, D4, D5, D6, D7, PAUSA, PI
    RS, E, D4, D5, D6, D7, PAUSA, PI = rs, e, d4, d5, d6, d7, pausa, pi
    # Configura los pines como salidas
    for pin in [RS, E, D4, D5, D6, D7]:
        PI.set_mode(pin, pigpio.OUTPUT)

def char2bin(char):
    '''Convierte un carácter en una representación binaria de 8 bits en orden específico y la retorna como una tupla de enteros.'''
    strink = bin(ord(char))[2:]
    strink = '0' * (8 - len(strink)) + strink  # Asegura que sea de 8 bits
    resultat = ''
    for bit in strink:
        resultat = bit + resultat  
    res = resultat[4:] + resultat[:4]
    tupla = tuple(int(element) for element in res)  # Convierte cada bit en entero y lo guarda en una tupla
    return tupla

def modecomandament(valor):
    '''Configura el modo de comando del display, ajustando el pin RS según si se está enviando una instrucción (False) o datos (True).'''
    if valor == False:
        PI.write(RS, 1)  
    else:
        PI.write(RS, 0)
    PI.write(E, 0)  

def escriu_a_fila_u():
    '''Mueve el cursor al inicio de la primera fila del display.'''
    modecomandament(True) 
    escriu4bits(0, 0, 0, 0)  
    escriu4bits(0, 0, 0, 0)
  
def escriu_a_fila_dos():
    '''Mueve el cursor al inicio de la segunda fila del display.'''
    modecomandament(True) 
    escriu4bits(0, 0, 1, 1)  
    escriu4bits(0, 0, 0, 0)

def escriu4bits(b1, b2, b3, b4):
    '''Envía 4 bits al display a través de los pines D4-D7.'''
    PI.write(D4, b1)
    PI.write(D5, b2)
    PI.write(D6, b3)
    PI.write(D7, b4)  
    time.sleep(PAUSA)
    PI.write(E, 1) 
    PI.write(E, 0)       
    time.sleep(PAUSA)

def esborra_la_pantalla():
    '''Envía la instrucción para borrar todo el display.'''
    modecomandament(True)
    time.sleep(PAUSA)
    escriu4bits(0, 0, 0, 0) 
    escriu4bits(1, 0, 0, 0) 

def envia_dades_al_display(dada):
    '''Envía un carácter (en forma de tupla de 8 bits) al display para ser mostrado.'''
    modecomandament(False) 
    escriu4bits(dada[0], dada[1], dada[2], dada[3]) 
    escriu4bits(dada[4], dada[5], dada[6], dada[7]) 

def detencio_pantalla():
    '''Pone el display en modo de detención o pausa.'''
    modecomandament(True) 
    escriu4bits(0, 0, 0, 0) 
    escriu4bits(0, 0, 1, 1) 

def inicia_pantalla():
    '''Configura el display para iniciarlo, estableciéndolo con dos filas y borrándolo.'''
    modecomandament(True)
    for _ in range(3):
        escriu4bits(1, 1, 0, 0)
    for _ in range(2):
        escriu4bits(0, 1, 0, 0)
    escriu4bits(1, 0, 1, 1)   
    escriu4bits(0, 0, 0, 0)
    escriu4bits(1, 1, 1, 1)
    esborra_la_pantalla()

def define_custom_char(location, pattern):
    '''Define un carácter personalizado en la posición `location` del LCD (0-7).
    `pattern` es una lista de 8 elementos donde cada elemento representa una fila
    de la matriz 5x8 en formato binario.'''
    location &= 0x07
    envia_comando(0x40 | (location << 3))

    for row in pattern:
        escriu4bits((row >> 4) & 0x01, (row >> 3) & 0x01, (row >> 2) & 0x01, (row >> 1) & 0x01)
        escriu4bits((row & 0x08) >> 3, (row & 0x04) >> 2, (row & 0x02) >> 1, row & 0x01)
        time.sleep(PAUSA)

def envia_comando(comando):
    '''Envía un comando al LCD (modo de comando en RS).'''
    modecomandament(True)
    escriu4bits((comando >> 4) & 0x01, (comando >> 3) & 0x01, (comando >> 2) & 0x01, (comando >> 1) & 0x01)
    escriu4bits((comando & 0x08) >> 3, (comando & 0x04) >> 2, (comando & 0x02) >> 1, comando & 0x01)
    time.sleep(PAUSA)
