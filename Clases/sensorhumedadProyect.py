import threading
import Adafruit_DHT  # Librería para el sensor DHT11
import time

class SensorDHT11(threading.Thread):
    '''Este apartado es para el sensor que mira los datos del DHT11 '''    
    def __init__(self, pin):
        super().__init__()
        self.dht_pin = dht_pin
        self.dht_sensor = Adafruit_DHT.DHT11
        
    def monitor(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
        if humidity is not None and temperature is not None:
            self.lcd_display.display_message(f"Temp: {temperature}C", f"Hum: {humidity}%")
            self.led_controller.leds(temperature)
            if temperature >= 30:
                self.motor_controller.control_motor(100)
            elif temperature >= 27:
                self.motor_controller.control_motor(100)
            else:
                self.motor_controller.control_motor(0)
            time.sleep(2)
