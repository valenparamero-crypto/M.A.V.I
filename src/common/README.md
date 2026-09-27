# 🔗 Común (Raspberry Pi + ESP32) — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

---

Recursos compartidos entre la Raspberry Pi y la ESP32: el mapa de registros I2C, que define el significado de cada comando y cada dato de estado intercambiado entre ambas tarjetas.

## 📁 Archivos

- `mapa_de_registros.md`: define el significado de cada casilla compartida entre las dos tarjetas.
- `protocol.py`: arma y verifica los mensajes según el mapa de registros (usa un checksum para detectar datos dañados).
- `bus_falso.py`: simula el comportamiento de la ESP32, para probar el protocolo mientras no hay acceso al hardware real.
- `prueba_protocolo.py`: script de prueba que demuestra que protocol.py y bus_falso.py funcionan juntos correctamente.

---

## 👤 Responsable

**Edwar Alfonso León** — Rol: Programación

Trabajo de esta semana 8: **Laura Valentina Paramero** (rotación de roles)

Formación Integral · Proyecto Integrador I · Proyecto Integrador II
Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2