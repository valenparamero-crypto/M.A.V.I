# 💻 Programación — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

Esta carpeta contiene el código fuente completo del proyecto M.A.V.I., organizado según la arquitectura de control distribuida entre la **Raspberry Pi 5** (procesamiento de alto nivel y visión) y la **ESP32-S3** (control de bajo nivel y sensores), además de los módulos compartidos para la comunicación sobre protocolo I2C.

---

## 📁 Estructura del Área

```text
src/
├── common/                               # Protocolo de comunicación, simulación y mapa de registros
│   ├── README.md
│   ├── bus_falso.py                      # Simulación del bus I2C para pruebas sin hardware
│   ├── mapa_de_registros.md              # Definición de direcciones y registros I2C
│   ├── protocol.py                       # Definición de estructuras y tramas del protocolo
│   └── prueba_protocolo.py               # Scripts de prueba y validación del protocolo
├── esp32/                                # Firmware de control de bajo nivel (ESP32-S3)
│   ├── README.md
│   ├── bascula_hx711.ino                 # Lectura de la celda de carga de 5 kg
│   ├── sketch_oct3a.ino                  # Integración de control y respuesta a comandos
│   └── sketch_sep29a_PruebaArranqueMotoresBlutuEncoders.ino # Validación de motores, encoders y Bluetooth
├── raspberry/                            # Código de alto nivel y visión (Raspberry Pi 5)
│   ├── README.md
│   ├── i2c_master.py                     # Gestión del bus I2C maestro (smbus2)
│   └── Test_Coml2C_RBP5-ESP32.py         # Pruebas de integración de comunicación
├── .gitignore
├── LICENSE
└── README.md                             # Documentación principal del área
```

---

## ⚙️ Arquitectura de Software y Protocolo

* **Procesamiento y Visión (Raspberry Pi 5):** Ejecución de algoritmos para adquisición de video con la cámara IMX219, reconocimiento de AprilTags y toma de decisiones en la navegación.
* **Control de Bajo Nivel (ESP32-S3):** Generación de señales PWM para el driver TB6612FNG, lectura de encoders de los motorreductores JGY370 y adquisición de datos de peso desde el módulo HX711.
* **Capa de Comunicación (Common):** Implementación de una arquitectura maestro-esclavo sobre bus I2C con mapa de registros modular, permitiendo enviar comandos de movimiento y consultar el estado del robot en tiempo real.

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Formación Integral · Proyecto Integrador I · Proyecto Integrador II · Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2