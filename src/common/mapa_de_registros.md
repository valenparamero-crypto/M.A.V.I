# Mapa de Registros I2C — M.A.V.I.

Este documento define el significado de cada "casilla" que la Raspberry Pi
y la ESP32 usan para comunicarse por I2C. Es la referencia oficial: si algo
cambia aquí, debe cambiar igual en el código de las dos tarjetas.

## Comandos (la Raspberry Pi escribe, la ESP32 lee)

| N.º | Nombre     | Valores                                                         | Descripción |
|-----|------------|------------------------------------------------------------------|-------------|
| 1   | Encendido  | 0 = apagado, 1 = encendido                                        | Prende o apaga el sistema de movimiento |
| 2   | Dirección  | 0 = quieto, 1 = adelante, 2 = atrás, 3 = izquierda, 4 = derecha   | Indica hacia dónde debe moverse el vehículo |

## Estado (la ESP32 escribe, la Raspberry Pi lee)

| N.º | Nombre | Valores                                       | Descripción |
|-----|--------|---------------------------------------------|-------------|
| 3   | Estado | 0 = hay un problema, 1 = cumpliendo la orden    | Indica si la ESP32 está ejecutando bien la orden recibida |

## Notas

- Este es un primer borrador (semana 8 del equipo). Falta agregar velocidad,
  lectura de encoders, sensores y manejo de obstáculos.
- Cualquier cambio a este mapa debe hablarse con Edwar (rol de Programación)
  antes de usarlo en el código, para que la Raspberry y la ESP32 no queden
  desincronizadas.