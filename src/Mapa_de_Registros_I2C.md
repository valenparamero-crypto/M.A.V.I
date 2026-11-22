<div align="center">

# 🔗 Mapa de registros I²C

![I2C](https://img.shields.io/badge/Protocolo-I%C2%B2C-1F6FB2?style=for-the-badge)
![Raspberry Pi 5](https://img.shields.io/badge/Maestro-Raspberry%20Pi%205-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white)
![ESP32-S3](https://img.shields.io/badge/Esclavo-ESP32--S3-E7352C?style=for-the-badge&logo=espressif&logoColor=white)

Define el lenguaje con el que se comunican la Raspberry Pi 5 y la ESP32-S3. Cada orden y cada respuesta viaja como un mensaje corto identificado por un número de registro. El código de ambas tarjetas debe seguir este mapa para que la comunicación funcione correctamente.

</div>

---

### ⚙️ Configuración del bus

- **Maestro** `Raspberry Pi 5` — Inicia toda la comunicación: envía órdenes y solicita datos.
- **Esclavo** `ESP32-S3` — Responde en la dirección `0x08`.
- **Bus** `I²C 1` — Raspberry Pi 5: `GPIO 2 (SDA)` · `GPIO 3 (SCL)` ↔ ESP32-S3: `GPIO 8 (SDA)` · `GPIO 9 (SCL)`.

---

### 🛡️ Verificación de los mensajes

Todos los mensajes terminan con un byte de verificación (*checksum*), que corresponde a la suma de los bytes anteriores, conservando solo los 8 bits menos significativos. Quien recibe el mensaje repite la suma y la compara: si no coincide, el mensaje se descarta, lo que evita que una orden alterada por ruido eléctrico llegue a los motores.

```text
checksum = (byte 1 + byte 2 + ... + byte n) & 0xFF
```

---

### 📤 Órdenes de la Raspberry Pi 5 a la ESP32-S3

#### Registro 1 · Encendido

```text
[ 1 | valor | checksum ]
```

Se envía al iniciar el programa (`valor = 1`) y al cerrarlo (`valor = 0`). Al recibirlo, la ESP32-S3 detiene los motores para que el vehículo arranque y termine siempre en reposo.

#### Registro 2 · Dirección

```text
[ 2 | dirección | checksum ]
```

Ordena un movimiento predefinido: `0` quieto · `1` adelante · `2` atrás · `3` izquierda · `4` derecha. En la versión actual se utiliza para detener el vehículo (`0`) como respaldo del registro 3.

#### Registro 3 · Velocidad de las ruedas

```text
[ 3 | velocidad izquierda | velocidad derecha | checksum ]
```

Fija la velocidad de cada rueda de forma independiente, lo que permite al controlador PID corregir la trayectoria de manera continua. Cada velocidad es un porcentaje entre `-100` y `100`, codificado como entero de 8 bits con signo: los valores positivos hacen avanzar la rueda y los negativos la hacen retroceder. Para no saturar el bus, la orden se envía solo cuando la velocidad cambia.

---

### 📥 Respuesta de la ESP32-S3 a la Raspberry Pi 5

#### Registro 0 · Telemetría

```text
[ estado | RPM izquierda | RPM derecha | checksum ]
```

La Raspberry Pi 5 solicita este registro cada 0.3 segundos para conocer el estado del vehículo:

- **Estado** — `1` si la ESP32-S3 recibió correctamente la última orden, `0` si llegó dañada.
- **RPM izquierda / derecha** — Velocidad de giro de cada motor, medida con los encoders.

La información se muestra en tiempo real sobre el video de la interfaz web.

---

<div align="center">
<sub><a href="README.md">⬅️ Volver a src</a></sub>
</div>