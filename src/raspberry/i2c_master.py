"""
Acceso real al bus I2C — M.A.V.I.
Corre solo en la Raspberry Pi 5, con Linux y el bus I2C habilitado.
No se puede probar en Windows ni sin el hardware conectado.

Requiere la libreria smbus2 (pip install smbus2).
"""

from smbus2 import SMBus
from src.common.protocol import armar_mensaje, verificar_mensaje, REG_ESTADO

# Direccion I2C de la ESP32 (debe coincidir con lo que programe Edwar/Juan en la ESP32)
DIRECCION_ESP32 = 0x08

# Numero del bus I2C de la Raspberry Pi 5 (normalmente es el 1)
NUMERO_BUS = 1


def escribir_registro(registro, valor):
    """
    Envia una orden real a la ESP32 por I2C.
    Arma el mensaje con el protocolo (mismo que usamos en las pruebas)
    y lo escribe en el bus de verdad.
    """
    trama = armar_mensaje(registro, valor)
    with SMBus(NUMERO_BUS) as bus:
        bus.write_i2c_block_data(DIRECCION_ESP32, trama[0], trama[1:])


def leer_estado():
    """
    Lee el registro de Estado de la ESP32 por I2C.
    Devuelve el valor de estado si el mensaje llego bien,
    o None si la respuesta llego danada.
    """
    with SMBus(NUMERO_BUS) as bus:
        trama = bus.read_i2c_block_data(DIRECCION_ESP32, REG_ESTADO, 3)

    if not verificar_mensaje(trama):
        print("[I2C REAL] Advertencia: la respuesta de la ESP32 llego danada")
        return None

    _, valor, _ = trama
    return valor