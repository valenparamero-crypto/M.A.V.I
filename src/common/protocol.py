"""
Protocolo de comunicación I2C — M.A.V.I.
Arma y verifica los mensajes según el mapa de registros
(ver mapa_de_registros.md en esta misma carpeta).
"""

# Casillas del mapa de registros
REG_ENCENDIDO = 1
REG_DIRECCION = 2
REG_ESTADO = 3


def armar_mensaje(registro, valor):
    """
    Arma una trama de 3 números: [registro, valor, checksum].
    El checksum es la suma de registro + valor.
    """
    checksum = registro + valor
    return [registro, valor, checksum]


def verificar_mensaje(trama):
    """
    Revisa si una trama llegó bien, comparando el checksum.
    Devuelve True si está bien, False si algo se dañó.
    """
    registro, valor, checksum_recibido = trama
    checksum_calculado = registro + valor
    return checksum_calculado == checksum_recibido