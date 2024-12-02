import pigpio
import time
from sensorhumedadProyect import SensorDHT11
from MotorProyect import Motor
from LEDsproyect import LEDs
from ComunicaProyect import MQ135, ZMPT101B, SCT013
import lcd_libProyect

def mostrar_en_lcd(lcd, linea1, linea2):
    """
    Muestra dos líneas de texto en el LCD.
    """
    lcd.esborra_la_pantalla()  # Borra la pantalla antes de escribir
    lcd.escriu_a_fila_u()  # Mueve el cursor a la primera fila
    for char in linea1[:8]:  # Máximo 8 caracteres en una línea
        lcd.envia_dades_al_display(lcd.char2bin(char))
    lcd.escriu_a_fila_dos()  # Mueve el cursor a la segunda fila
    for char in linea2[:8]:  # Máximo 8 caracteres en una línea
        lcd.envia_dades_al_display(lcd.char2bin(char))

def main():
    # Configuración de pigpio
    pi = pigpio.pi()  # Instancia de pigpio
    if not pi.connected:
        print("El pigpio no está corriendo. Revisa las conexiones.")
        return

    # Configuración de pines
    pin_dht11 = 6         # GPIO6 para el sensor DHT11
    en_pin = 18           # GPIO18 para habilitación del motor
    in1_pin = 17          # GPIO17 dirección 1 del motor
    in2_pin = 27          # GPIO27 dirección 2 del motor
    pin_mq135 = 22        # GPIO22 para la salida digital del MQ135
    pines_leds = {        # LEDs
        "verde": 16,      # GPIO16 
        "amarillo": 20,   # GPIO20 
        "rojo": 21        # GPIO21 
    }

    # Configuración del LCD
    rs, e, d4, d5, d6, d7 = 4, 5, 25, 24, 23, 12  # Pines según tu tabla
    pausa = 0.002
    lcd_libProyect.inicialitza_pins(rs, e, d4, d5, d6, d7, pausa, pi)
    lcd_libProyect.inicia_pantalla()

    # Configuración del ADC (MQ135, SCT-013, ZMPT101B)
    from Adafruit_ADS1x15 import ADS1115
    adc = ADS1115(address=0x48, busnum=1)
    sensor_corriente = SCT013(adc=adc, canal=1)
    sensor_voltaje = ZMPT101B(adc=adc, canal=0)

    # Inicialización de sensores y dispositivos
    sensor_dht = SensorDHT11(pin=pin_dht11)
    motor = Motor(en_pin=en_pin, in1_pin=in1_pin, in2_pin=in2_pin, pi=pi)
    leds = LEDs(pines=pines_leds, pi=pi)
    mq135 = MQ135(pin=pin_mq135, pi=pi)

    # Iniciar hilos para sensores
    sensor_dht.start()  # Inicia el hilo para el sensor DHT11
    mq135.start()
    sensor_corriente.start()
    sensor_voltaje.start()

    try:
        while True:
            # Obtener datos del sensor DHT11
            temperatura = sensor_dht.temperature
            humedad = sensor_dht.humedad

            if temperatura is not None and humedad is not None:
                print(f"Temperatura: {temperatura}°C, Humedad: {humedad}%")

                # Mostrar en el LCD
                corriente = sensor_corriente.corriente if sensor_corriente.corriente is not None else 0.0
                voltaje = sensor_voltaje.voltaje if sensor_voltaje.voltaje is not None else 0.0
                potencia = corriente * voltaje
                linea1 = f"T:{temperatura:.1f}C H:{humedad:.1f}%"
                linea2 = f"I:{corriente:.1f} V:{voltaje:.1f} P:{potencia:.1f}"
                mostrar_en_lcd(lcd_libProyect, linea1, linea2)

                # Control de LEDs según la temperatura
                leds.controlar_leds(temperatura)

                # Control del motor según la temperatura
                if temperatura > 30:
                    motor.activar()
                else:
                    motor.desactivar()

            # Estado del MQ135
            estado_gas = mq135.estado_gas  # 0: Gas detectado, 1: No detectado
            print(f"Estado del Gas: {'Detectado' if estado_gas == 0 else 'No detectado'}")

            # Monitoreo de consumo energético
            if sensor_corriente.corriente is not None and sensor_voltaje.voltaje is not None:
                print(f"Consumo Actual: {potencia:.2f} W")

            time.sleep(3)

    except KeyboardInterrupt:
        # Limpieza al salir
        print("Deteniendo el programa y limpiando recursos...")
        motor.desactivar()
        leds.apagar_todos()
        leds.limpiar()
        pi.stop()
        print("\nPrograma terminado.")

if __name__ == "__main__":
    main()
