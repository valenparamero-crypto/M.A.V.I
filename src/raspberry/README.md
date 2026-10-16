# 🧠 Raspberry Pi 5 — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

---

Código que corre en la Raspberry Pi 5: captura de video con cámara IMX219, procesamiento de visión por computador (seguimiento de carril, detección de obstáculos y lectura de AprilTags), lógica de decisiones y envío de comandos maestros a la ESP32 mediante el protocolo I2C.

---

## 📁 Estructura de la Carpeta

```text
raspberry/
├── i2c_master.py                          # Script maestro para la gestión de comunicación I2C (smbus2)
├── mavi_apriltags.py              # # Módulo principal de visión por computador, detección de carril, obstáculos y AprilTags
├── Test_Coml2C_RBP5-ESP32.py              # Script de pruebas y validación de comunicación I2C entre RPi5 y ESP32
└── README.md                              # Documentación del subsistema de procesamiento y visión
```

---

## 💻 Descripción de los Scripts

* **mavi_apriltags.py`:** Módulo de visión por computador e inicialización del hardware con la librería `Picamera2` y `OpenCV`. Integra la segmentación HSV para seguimiento del carril (líneas roja y amarilla), estimación de horizonte visual, algoritmo Canny para la detección de obstáculos en zona baja y decodificación de marcas fiduciales AprilTags `(DICT_APRILTAG_36h11)` para guiado autónomo y eventos de navegación.
* **`i2c_master.py`:** Implementa la interfaz maestra de comunicación sobre el bus I2C utilizando la librería `smbus2` para el envío de tramas de control hacia el microcontrolador de bajo nivel.
* **`Test_Coml2C_RBP5-ESP32.py`:** Script orientado a pruebas de integración hardware/software para verificar la estabilidad y el intercambio correcto de paquetes de datos entre la Raspberry Pi 5 y la ESP32.

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Formación Integral · Proyecto Integrador I · Proyecto Integrador II
Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2