import pigpio
import time

from LEDsproyect import LEDs
import lcd_libProyect  # Asegúrate de usar el nombre correcto de la librería

def main():
    # Configuración de pigpio
    pi = pigpio.pi()  # Instancia de pigpio
    if not pi.connected:
        print("El pigpio no está corriendo revisa coño.")
        return

    # Configuración de pines para los LEDs
    pines_leds = {        # LEDs
        "verde": 16,      # GPIO16 
        "amarillo": 20,   # GPIO20 
        "rojo": 21        # GPIO21 
    }
    leds = LEDs(pines=pines_leds, pi=pi)  # Instancia de la clase LEDs

    # Configuración del LCD
    rs, e, d4, d5, d6, d7 = 4, 5, 25, 24, 23, 12  # Pines según tu tabla
    pausa = 0.002
    lcd_libProyect.inicialitza_pins(rs, e, d4, d5, d6, d7, pausa, pi)
    lcd_libProyect.inicia_pantalla()

    try:
        # Prueba del LCD y los LEDs
        lcd_libProyect.esborra_la_pantalla()
        mensaje = "Hola, Patito!"
        for char in mensaje:
            lcd_libProyect.envia_dades_al_display(lcd_libProyect.char2bin(char))
        time.sleep(2)

        # Encender los LEDs en secuencia
        leds.encender("rojo")
        time.sleep(2)
        leds.encender("amarillo")
        time.sleep(2)
        leds.encender("verde")
        time.sleep(2)
        leds.apagar_todos()

    except KeyboardInterrupt:
        # Limpieza al salir
        leds.apagar_todos()
        pi.stop()  # Detener pigpio
        print("\nAdiós miserable usuario.")

if __name__ == "__main__":
    main()
