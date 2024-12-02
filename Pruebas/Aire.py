import pigpio
import time

from ComunicaProyect import MQ135


def main():
    # Configuración de pigpio
    pi = pigpio.pi()  # Instancia de pigpio
    if not pi.connected:
        print("El pigpio no está corriendo revisa coño.")
        return



    # Configuración del ADC (MQ135, SCT-013, ZMPT101B)
    from Adafruit_ADS1x15 import ADS1115
    adc = ADS1115(address=0x48, busnum=2)
    mq135 = MQ135(adc=adc, canal=0)
    
    # Inicio hilos

    mq135.start()
    
    # Me pongo a hacer una oración para que todo resulte :D 
    
    try:
        while True:
                           
            # Monitoreo de calidad del aire
            if mq135.calidad_aire > 400:  # Umbral crítico
                print("¡Alerta! Calidad del aire crítica")

            time.sleep(2)

    except KeyboardInterrupt:
        # Limpieza al salir
        pi.stop()  # Detener pigpio
        print("\nAdiós miserable usuario.")

if __name__ == "__main__":
    main()
