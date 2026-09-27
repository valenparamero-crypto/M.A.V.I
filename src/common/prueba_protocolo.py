"""
Prueba manual del protocolo I2C con el bus simulado.
Ejecutar con: python -m src.common.prueba_protocolo
"""

from .protocol import armar_mensaje
from .bus_falso import BusI2CFalso

bus = BusI2CFalso()

print("--- Caso 1: mensaje correcto (encender) ---")
mensaje = armar_mensaje(1, 1)
bus.enviar(mensaje)
print("Estado tras el mensaje:", bus.leer_estado())

print("\n--- Caso 2: mensaje dañado (checksum incorrecto) ---")
mensaje_malo = [1, 3, 2]
bus.enviar(mensaje_malo)
print("Estado tras el mensaje:", bus.leer_estado())