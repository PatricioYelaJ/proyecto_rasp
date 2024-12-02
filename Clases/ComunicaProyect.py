from Adafruit_ADS1x15 import ADS1115
import threading
import time
import pigpio


# Clase para el sensor MQ135 con salida digital
class MQ135(threading.Thread):
    """
    Clase para manejar el sensor MQ135 utilizando su salida digital.
    """
    def __init__(self, pin, pi):
        """
        Inicializa el sensor MQ135.

        :param pin: Pin GPIO conectado a la salida digital del MQ135.
        :param pi: Instancia de pigpio.pi().
        """
        super().__init__()
        self.pin = pin
        self.pi = pi  # Instancia de pigpio
        self.pi.set_mode(self.pin, pigpio.INPUT)  # Configura el pin como entrada
        self.estado_gas = None  # Estado del gas (0 o 1)

    def leer_estado_gas(self):
        """
        Lee el estado del gas desde el pin digital.

        :return: 0 si se detecta gas, 1 si no se detecta gas.
        """
        self.estado_gas = self.pi.read(self.pin)
        return self.estado_gas

    def run(self):
        """
        Loop principal para actualizar el estado del sensor periódicamente.
        """
        while True:
            self.leer_estado_gas()
            print(f"MQ135 Estado del Gas: {'Detectado' if self.estado_gas == 0 else 'No detectado'}")
            time.sleep(1)  # Ajusta el intervalo según sea necesario


# Clase para leer voltaje con el ZMPT101B
class ZMPT101B(threading.Thread):
    """
    Este apartado es para el sensor que mide el voltaje.
    """
    def __init__(self, adc, canal, gain=1):
        super().__init__()
        self.adc = adc
        self.canal = canal
        self.gain = gain
        self.voltaje = None

    def leer_voltaje(self):
        """
        Lee el voltaje desde el ADC.
        """
        valor = self.adc.read_adc(self.canal, gain=self.gain)
        self.voltaje = valor / 1000  # Ajusta según el divisor del circuito
        return self.voltaje

    def run(self):
        """
        Loop principal para actualizar el voltaje periódicamente.
        """
        while True:
            self.leer_voltaje()
            print(f"ZMPT101B Voltaje: {self.voltaje} V")
            time.sleep(2)


# Clase para leer corriente con el SCT-013
class SCT013(threading.Thread):
    """
    Este apartado es para el sensor de corriente.
    """
    def __init__(self, adc, canal, gain=1):
        super().__init__()
        self.adc = adc
        self.canal = canal
        self.gain = gain
        self.corriente = None

    def leer_corriente(self):
        """
        Lee la corriente desde el ADC.
        """
        valor = self.adc.read_adc(self.canal, gain=self.gain)
        self.corriente = valor / 1000  # Conversión según el rango del sensor
        return self.corriente

    def run(self):
        """
        Loop principal para actualizar la corriente periódicamente.
        """
        while True:
            self.leer_corriente()
            print(f"SCT-013 Corriente: {self.corriente} A")
            time.sleep(2)
