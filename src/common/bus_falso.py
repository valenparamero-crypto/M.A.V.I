"""
Bus I2C simulado — M.A.V.I.
Se usa mientras no hay acceso a la Raspberry Pi 5 real.
Se comporta parecido al bus I2C, pero solo en la memoria del computador.
"""

from .protocol import verificar_mensaje, REG_ESTADO


class BusI2CFalso:
    """
    Simula el bus I2C: recibe mensajes y responde como si fuera la ESP32.
    """

    def __init__(self):
        self.estado_actual = 1  # 1 = cumpliendo la orden

    def enviar(self, trama):
        """
        Simula el envío de una trama por el bus.
        Si el checksum no cuadra, la ESP32 (falsa) rechaza el mensaje.
        """
        if not verificar_mensaje(trama):
            print(f"[BUS FALSO] Mensaje rechazado (checksum inválido): {trama}")
            self.estado_actual = 0
            return False

        registro, valor, _ = trama
        print(f"[BUS FALSO] ESP32 recibió: registro={registro}, valor={valor}")
        self.estado_actual = 1
        return True

    def leer_estado(self):
        """
        Simula la lectura del registro de Estado (registro 3).
        """
        return [REG_ESTADO, self.estado_actual, REG_ESTADO + self.estado_actual]