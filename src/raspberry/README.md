# 🧠 Raspberry Pi 5 — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

---

Código que corre en la Raspberry Pi 5: captura de video con cámara IMX219, procesamiento de visión por computador, detección de AprilTags, lógica de decisiones y envío de comandos maestros a la ESP32 mediante protocolo I2C.

---

## 📁 Estructura de la Carpeta

```text
raspberry/
├── i2c_master.py                          # Script maestro para la gestión de comunicación I2C (smbus2)
├── Test_Coml2C_RBP5-ESP32.py              # Script de pruebas y validación de comunicación I2C entre RPi5 y ESP32
└── README.md                              # Documentación del subsistema de procesamiento y visión
```

---

## 💻 Descripción de los Scripts

* **`i2c_master.py`:** Implementa la interfaz maestra de comunicación sobre el bus I2C utilizando la librería `smbus2` para el envío de tramas de control hacia el microcontrolador de bajo nivel.
* **`Test_Coml2C_RBP5-ESP32.py`:** Script orientado a pruebas de integración hardware/software para verificar la estabilidad y el intercambio correcto de paquetes de datos entre la Raspberry Pi 5 y la ESP32.

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Formación Integral · Proyecto Integrador I · Proyecto Integrador II
Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2