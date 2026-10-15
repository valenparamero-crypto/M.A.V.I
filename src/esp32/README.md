# ⚙️ ESP32 — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

Firmware de la ESP32: control de motores, lectura de encoders y sensores, gestión de báscula (HX711) y ejecución de los comandos recibidos de la Raspberry Pi mediante protocolo I2C.

---

## 📁 Estructura de la Carpeta

```text
esp32/
├── bascula_hx711.ino                      # Código para adquisición de peso con celda de carga y HX711
├── sketch_oct3a.ino                       # Script de pruebas y control general del sistema
├── sketch_sep29a_PruebaArranqueMotoresBlutuEncoders.ino # Pruebas iniciales de arranque de motores, encoders y conectividad
└── README.md                              # Documentación del subsistema de microcontrolador
```

---

## 💻 Descripción de los Programas (Sketches)

* **`bascula_hx711.ino`:** Implementa la lectura de la celda de carga de 5 kg a través del conversor A/D HX711 para el subsistema de pesaje de M.A.V.I.
* **`sketch_sep29a_PruebaArranqueMotoresBlutuEncoders.ino`:** Rutinas iniciales para la validación física del arranque de los motorreductores con driver TB6612FNG, lectura de encoders y pruebas de comunicación inalámbrica.
* **`sketch_oct3a.ino`:** Script estructurado para la integración del control de bajo nivel y la respuesta a los comandos maestros de la Raspberry Pi.

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Formación Integral · Proyecto Integrador I · Proyecto Integrador II
Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2