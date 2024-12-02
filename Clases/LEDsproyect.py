import pigpio
import time
import threading

class LEDs(threading.Thread):
    """
    Clase para controlar LEDs usando pigpio.
    """
    def __init__(self, pines, pi):
        """
        Inicializa la clase LEDs.

        :param pines: Diccionario con los pines de los LEDs (ej: {"verde": 16, "amarillo": 20, "rojo": 21}).
        :param pi: Instancia de pigpio.pi().
        """
        super().__init__()
        self.pines = pines  # Diccionario de pines ("verde", "amarillo", "rojo")
        self.pi = pi        # Instancia de pigpio
        self._detener = threading.Event()  # Bandera para detener el hilo

        # Configura los pines como salida
        for pin in self.pines.values():
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, 0)  # Apaga los LEDs inicialmente

    def controlar_leds(self, temperature):
        """
        Controla los LEDs según el rango de temperatura.

        :param temperature: La temperatura actual.
        """
        if temperature <= 27:
            self.pi.write(self.pines["verde"], 1)
            self.pi.write(self.pines["amarillo"], 0)
            self.pi.write(self.pines["rojo"], 0)
        elif 27.1 <= temperature <= 30:
            self.pi.write(self.pines["verde"], 0)
            self.pi.write(self.pines["amarillo"], 1)
            self.pi.write(self.pines["rojo"], 0)
        else:
            self.pi.write(self.pines["verde"], 0)
            self.pi.write(self.pines["amarillo"], 0)
            self.pi.write(self.pines["rojo"], 1)

    def apagar_todos(self):
        """
        Apaga todos los LEDs.
        """
        for pin in self.pines.values():
            self.pi.write(pin, 0)
        print("[LED] Todos apagados")

    def detener(self):
        """
        Detiene el hilo y apaga todos los LEDs.
        """
        self._detener.set()

    def run(self):
        """
        Loop principal del hilo.
        """
        while not self._detener.is_set():
            time.sleep(1)
        self.apagar_todos()
        print("[LEDs] Hilo detenido.")

    def limpiar(self):
        """
        Detiene el cliente de pigpio (opcional, en caso de que sea exclusivo de esta clase).
        """
        self.pi.stop()
        print("[LEDs] Cliente de pigpio detenido.")
