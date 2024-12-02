import pigpio
import time
from sensorhumedadProyect import SensorDHT11
from MotorProyect import Motor
from LEDsproyect import LEDs
from ComunicaProyect import MQ135, ZMPT101B, SCT013
from lcd_libProyect import *

def mostrar_en_lcd(linea1, linea2):
    """
    Muestra dos líneas de texto en el LCD.
    """
    esborra_la_pantalla()                       # Borra la pantalla antes de escribir
    escriu_a_fila_u()                           # Mueve el cursor a la primera fila
    for char in linea1[:16]:                    # Máximo 16 caracteres en una línea
        envia_dades_al_display(char2bin(char))
    escriu_a_fila_dos()                         # Mueve el cursor a la segunda fila
    for char in linea2[:16]:                    # Máximo 16 caracteres en una línea
        envia_dades_al_display(char2bin(char))

def main():
    # Configuración de pigpio
    pi = pigpio.pi()                            # Instancia de pigpio
    if not pi.connected:
        print("El pigpio no está corriendo. Revisa el servicio.")
        return

    # Configuración de pines
    en_pin = 18           # GPIO18 para habilitación del motor
    in1_pin = 6           # GPIO17 dirección 1 del motor
    in2_pin = 27          # GPIO27 dirección 2 del motor
    pin_mq135 = 22
    pines_leds = {        # LEDs
        "verde": 16,      # GPIO16 
        "rojo": 21        # GPIO21 
    }

    # Configuración del LCD
    rs, e, d4, d5, d6, d7 = 4, 5, 25, 24, 23, 12    # Pines según tu tabla
    pausa = 0.002
    inicialitza_pins(rs, e, d4, d5, d6, d7, pausa)  # Inicialización de los pines del LCD
    inicia_pantalla()                               # Inicia el LCD

    # Configuración del ADC (MQ135, SCT-013, ZMPT101B)
    from Adafruit_ADS1x15 import ADS1115
    adc = ADS1115(address=0x48, busnum=1)
    sensor_corriente = SCT013(adc=adc, canal=1)
    sensor_voltaje = ZMPT101B(adc=adc, canal=0)

    # Inicialización de sensores y dispositivos
    motor = Motor(en_pin=en_pin, in1_pin=in1_pin, in2_pin=in2_pin, pi=pi)
    leds = LEDs(pines=pines_leds, pi=pi)
    mq135 = MQ135(pin=pin_mq135, pi=pi)             # MQ135 con salida digital

    # Iniciar hilos para sensores
    mq135.start()
    sensor_corriente.start()
    sensor_voltaje.start()
    
    try:
        while True:

            # Estado del MQ135
            estado_gas = mq135.estado_gas           # 0: Gas detectado, 1: No detectado
            estado_gas_str = "RUN!" if estado_gas == 0 else "0GAS"
           
            # Monitoreo de consumo energético
            if sensor_corriente.corriente is not None and sensor_voltaje.voltaje is not None:
                corriente = sensor_corriente.corriente
                voltaje = sensor_voltaje.voltaje
                potencia = corriente * voltaje/1000
                mensaje_1 = f"I:{corriente:.2f}A V:{voltaje}V"
                mensaje_2 = f"P:{potencia:.1f}kW Gas:{estado_gas_str}"
                mostrar_en_lcd(mensaje_1, mensaje_2)
            
            time.sleep(2)
            
            if estado_gas == 0:
                leds.pi.write(leds.pines["verde"], 0)
                leds.pi.write(leds.pines["rojo"], 1)
                motor.girar_derecha()
                
            else:
                leds.pi.write(leds.pines["verde"], 1)
                leds.pi.write(leds.pines["rojo"], 0)
                motor.parar()
                

            time.sleep(2)

    except KeyboardInterrupt:
        # Limpieza al salir
        print("Deteniendo el programa y limpiando recursos...")
        motor.parar()
        leds.apagar_todos()
        pi.stop()                                   # Detener pigpio
        print("\nAdiós miserable usuario.")

if __name__ == "__main__":
    main()
