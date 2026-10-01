# 💻 Programación — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

---

Esta carpeta contiene el código fuente de M.A.V.I., organizado por tarjeta y por los módulos compartidos entre sí.

## 📁 Estructura

```text
src/
├── common/                # Compartido: mapa de registros y protocolo I2C
│   ├── README.md
│   ├── bus_falso.py
│   ├── mapa_de_registros.md
│   ├── protocol.py
│   └── prueba_protocolo.py
├── esp32/                 # Firmware de la ESP32 (motores, sensores)
│   └── README.md
├── raspberry/             # Código de la Raspberry Pi 5 (visión, QR, decisiones)
│   ├── README.md
│   └── i2c_master.py
├── .gitignore
├── LICENSE
└── README.md
```

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Formación Integral · Proyecto Integrador I · Proyecto Integrador II · Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2