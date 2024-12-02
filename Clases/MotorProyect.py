import pigpio
import time
import threading

class Motor(threading.Thread):
    def __init__(self, en_pin, in1_pin, in2_pin, pi):
        """
        Clase para controlar un motor DC utilizando pigpio.
        
        Parámetros:
        - en_pin: Pin GPIO para habilitar el motor.
        - in1_pin: Pin GPIO para controlar la dirección (entrada 1).
        - in2_pin: Pin GPIO para controlar la dirección (entrada 2).
        - pi: Instancia de pigpio.pi().
        """
        super().__init__()
        self.pi = pi
        self.en_pin = en_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Configuración de los pines como salida
        self.pi.set_mode(self.en_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.in1_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.in2_pin, pigpio.OUTPUT)

        self.estado = "parado"  # Estado inicial: 'derecha', 'izquierda' o 'parado'

    def girar_derecha(self):
        """Activa el motor para girar a la derecha."""
        self.pi.write(self.en_pin, 1)
        self.pi.write(self.in1_pin, 0)
        self.pi.write(self.in2_pin, 1)
        self.estado = "derecha"
        print("Motor girando")

    def parar(self):
        """Detiene el motor."""
        self.pi.write(self.en_pin, 0)
        self.pi.write(self.in1_pin, 0)
        self.pi.write(self.in2_pin, 0)
        self.estado = "parado"
        

    def run(self):
        """
        Método del hilo que puede ser personalizado según la lógica del programa.
        """
        while True:
            if self.estado == "derecha":
                print("Motor en funcionamiento: Girando a la derecha.")
            elif self.estado == "parado":
                print("Motor en reposo.")
            time.sleep(2)  # Ajustar tiempo según la necesidad
