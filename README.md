<div align="center">

# 🤖 M.A.V.I. — Módulo Autónomo de Visión Inteligente

**Vehículo Guiado Automáticamente (AGV) con plataforma holonómica y visión artificial**

**Facultad de Tecnología**
**Universidad Tecnológica de Pereira**
**Programa de Ingeniería Mecatrónica**
**Semestre Integrador — Proyecto Integrador I y II · 2026-2**
**Grupo #** _(completar)_

</div>

---

## 👥 Integrantes

| Nombre | Rol principal |
| :--- | :--- |
| **Juan Miguel Noreña** | Líder técnico / Electrónica |
| **Sara Edith Perilla** | Diseño mecánico |
| **Edwar Alfonso León** | Programación |
| **Laura Valentina Paramero** | Documentación |

> En el equipo los roles rotan entre áreas según la semana; la tabla muestra el área de la que cada persona es responsable.

---

## 📌 Introducción

**M.A.V.I.** es un Vehículo Guiado Automáticamente (AGV) pensado para el transporte interno de cargas de hasta **1 kg** entre estaciones de carga y descarga, sobre una pista compartida con otros equipos. El vehículo sigue la pista con una cámara, reconoce cada estación mediante **AprilTags** ubicados en soportes verticales, detecta si lleva carga encima y se comunica con las estaciones por señales infrarrojas.

El proyecto integra cuatro áreas:

### 🔧 Diseño mecánico
Chasis diseñado en **Autodesk Fusion 360** inspirado en robots logísticos tipo Amazon Kiva. La base usa **2 ruedas holonómicas tipo Mecanum** (rodillos a 45°) con tracción diferencial y **4 ruedas locas** de apoyo. Se validó primero con prototipos en MDF y luego con piezas impresas en 3D (resina SLA y FDM) para soportes de motores y ruedas locas.

### ⚡ Electrónica y potencia
Batería **LiPo de 7.4 V / 5000 mAh**, con un regulador reductor **XL4016** que entrega 5.1 V a la Raspberry Pi 5, la ESP32-S3 y la lógica del driver. Los motores **JGY-370 con encoder** se controlan con el driver **TB6612FNG**. Todo se consolida en una **PCB propia** diseñada en Fusion 360. Incluye switch general y pulsador de paro de emergencia.

### 🎛️ Control y movimiento
La **ESP32-S3** hace el control de bajo nivel: genera el PWM de los motores, lee los encoders, el giroscopio/acelerómetro **BMI270**, el sensor de distancia **VL53L1X**, la celda de carga (**HX711**) y el par infrarrojo. Recibe órdenes de la Raspberry Pi 5 por **I²C** (Raspberry = maestro, ESP32 = esclavo) usando un mapa de registros propio.

### 👁️ Visión por computador
La **Raspberry Pi 5** procesa en Python el video de la cámara **IMX219 (162° FOV)**: detecta las líneas de la pista, reconoce los **AprilTags** de las estaciones y detecta obstáculos (el VL53L1X mide la distancia para decidir si parar). Con esa información toma las decisiones de navegación y se las envía a la ESP32-S3.

---

## 🎯 Objetivo general

Desarrollar un vehículo guiado automáticamente (AGV) que integre una plataforma holonómica y visión artificial, con capacidad para transportar cargas de hasta 1 kg entre estaciones predefinidas de carga y descarga en una pista compartida, antes de finalizar el semestre académico 2026-2.

---

## 🧰 Materiales y tecnologías principales

### Materiales electrónicos

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Raspberry Pi 5 (8 GB) | Computador de placa única | Procesamiento de alto nivel: visión artificial y toma de decisiones |
| Cámara IMX219-160 | Cámara de 8 MP, 162° FOV, conexión CSI | Captura de la pista, AprilTags y obstáculos |
| ESP32-S3 N16R8 | Microcontrolador de doble núcleo | Control de bajo nivel de motores y lectura de sensores |
| Driver TB6612FNG | Puente H doble | Controla velocidad y sentido de giro de los dos motores |
| Motorreductor JGY-370 (x2) | Motor 6 V, 100 RPM, con encoder | Tracción del vehículo y medición de giro de las ruedas |
| Batería LiPo 7.4 V 5000 mAh | Batería de litio-polímero 2S | Fuente de energía de todo el sistema |
| Regulador XL4016 | Convertidor DC-DC reductor (step-down) | Baja de 7.4 V a 5.1 V para la electrónica |
| BMI270 | Unidad de medición inercial (SPI) | Mide giros y aceleraciones del vehículo |
| VL53L1X (módulo TOF400C) | Sensor láser de distancia, hasta 4 m | Mide la distancia a obstáculos |
| Celda de carga 3 kg + HX711 | Sensor de peso y conversor A/D de 24 bits | Detecta si hay carga sobre el vehículo |
| Par infrarrojo (emisor/receptor) | LED IR y receptor IR | Intercambio de señales con las estaciones |
| Pulsador de paro de emergencia | Pulsador normalmente abierto | Detiene los motores ante un riesgo |
| Ventilador 5 V | Ventilador pequeño | Enfría el regulador XL4016 |
| PCB M.A.V.I. | Placa de circuito impreso propia | Integra la distribución de potencia y las conexiones de señal |

### Materiales mecánicos

| Componente | Material | Método de fabricación | Observaciones |
| :--- | :--- | :--- | :--- |
| Chasis prototipo | MDF | Corte láser | Usado para validar medidas y montaje |
| Chasis final | _(completar)_ | _(completar)_ | Modelo integral `v2` en Fusion 360 |
| Soportes de motores | Resina / PLA | Impresión 3D (SLA / FDM) | Fijan los JGY-370 al chasis |
| Acoples de rueda | Resina | Impresión 3D (SLA) | Unen el eje del motor con la rueda Mecanum |
| Soportes de ruedas locas | PLA | Impresión 3D (FDM) | 4 puntos de apoyo |
| Ruedas Mecanum 60 mm (x2) | Comercial | Compradas | Rodillos a 45° |
| Ruedas locas (x4) | Comercial | Compradas | Estabilidad del vehículo |
| Tornillería | Acero | Comercial | _(completar medidas)_ |

### Herramientas utilizadas

| Herramienta | Tipo | Función principal |
| :--- | :--- | :--- |
| Autodesk Fusion 360 | Software CAD / EDA | Diseño del chasis, piezas y PCB |
| Arduino IDE | Entorno de programación | Firmware en C++ de la ESP32-S3 |
| Python 3 | Lenguaje de programación | Visión artificial y comunicación en la Raspberry Pi 5 |
| OpenCV + librería AprilTag | Librerías de visión | Detección de la pista y de los AprilTags |
| Raspberry Pi OS | Sistema operativo | Base de la Raspberry Pi 5 |
| Impresora 3D (SLA / FDM) | Máquina de fabricación | Fabricación de soportes y acoples |
| Cortadora láser | Máquina de fabricación | Corte de piezas en MDF |
| Multímetro / fuente de laboratorio | Instrumentos de medición | Pruebas eléctricas |
| Git y GitHub | Control de versiones | Trabajo colaborativo y trazabilidad |
| Microsoft Excel (Gantt) | Software de planeación | Cronograma y ruta crítica |

---

## 📁 Áreas de desarrollo (estructura del repositorio)

```text
M.A.V.I./
├── documentación/        → Planeación y gestión del proyecto
├── diseño electrónico/   → Esquemas, PCB y evidencias de electrónica
├── diseño mecánico/      → CAD del chasis y evidencias de fabricación
├── src/                  → Código fuente (software)
├── LICENSE
└── README.md
```

### 📄 Documentación / planeación
Acta de constitución, propuesta formal, cronograma (`GANTT.xlsx`), ruta crítica (CPM) y bitácoras de planeación y ejecución (semanas 8 a 14), en normas APA 7.ª edición.

### ⚡ Diseño electrónico
Diagrama de bloques, tabla de conexiones, esquema electrónico, diseño de la PCB (`PCB/mavi_pcb_diseno_integral.f3z`) y evidencias de pruebas (banco de pruebas de la ESP32, cámara, detección de AprilTags, reconocimiento de pista).

### 🔧 Diseño mecánico
Modelos CAD (`v1_inicial/` y modelo integral `v2`), diseño conceptual con listado de materiales y evidencias de fabricación (MDF, impresión 3D, ensamble de ruedas).

### 💻 SRC (software)

```text
src/
├── common/     → Protocolo I²C compartido: mapa de registros, protocol.py,
│                 bus simulado (bus_falso.py) y pruebas
├── esp32/      → Firmware C++: motores, encoders y báscula HX711
└── raspberry/  → Python: maestro I²C y pruebas de comunicación con la ESP32
```

---

## 📚 Asignaturas relacionadas

| Asignatura | Aporte al proyecto |
| :--- | :--- |
| **Programación** | Firmware de la ESP32-S3 (C++) y software de la Raspberry Pi 5 (Python) |
| **Electrónica analógica y digital** | Acondicionamiento de sensores, lógica de 3.3 V, buses I²C y SPI |
| **Electrónica de potencia** | Regulación de voltaje con el XL4016 y control de motores con el TB6612FNG |
| **Inteligencia artificial** | Visión por computador para el seguimiento de pista y detección de obstáculos |
| **Automatización industrial** | Concepto de AGV para logística interna y comunicación con estaciones |
| **Dibujo técnico** | Modelado CAD, planos y ensamble del chasis |

---

## 🌱 Beneficios esperados

- Demostrar a escala cómo funciona el transporte interno automatizado usado en manufactura y logística.
- Integrar en un solo prototipo lo aprendido en mecánica, electrónica, control, programación y visión artificial.
- Dejar una arquitectura modular (Raspberry Pi 5 + ESP32-S3 por I²C) que otros equipos puedan reutilizar o ampliar.
- Documentar todo el proceso (diseño, fabricación, pruebas y gestión) para que el proyecto sea replicable.
- Fortalecer el trabajo en equipo y la gestión de proyectos con herramientas reales (Gantt, CPM, bitácoras).

---

## 📊 Estado actual del proyecto

| Módulo | Estado | Avance |
| :--- | :---: | :--- |
| 🔧 Módulo mecánico | 🟡 En proceso | Chasis `v2` modelado; soportes y acoples impresos en 3D; ensamble de ruedas Mecanum y ruedas locas validado. |
| ⚡ Módulo electrónico | 🟡 En proceso | Tabla de conexiones v3.2 y diagrama de bloques actualizados; PCB diseñada y enviada a fabricación. |
| 🎛️ Módulo de control y software (SRC) | 🟡 En proceso | Comunicación I²C Raspberry Pi 5 → ESP32-S3 verificada; control de motores con encoders y báscula HX711 probados; detección de pista y AprilTags en fase de prueba. |
| 📄 Módulo de documentación | 🟡 En proceso | Acta, propuesta, Gantt, CPM y bitácoras (semanas 8–14) completas; artículo en formato HardwareX en desarrollo. |

> 🟢 Finalizado · 🟡 En proceso · 🔴 Pendiente

---

## 🏅 Créditos

Proyecto desarrollado por **Juan Miguel Noreña, Sara Edith Perilla, Edwar Alfonso León y Laura Valentina Paramero**, estudiantes de Ingeniería Mecatrónica de la **Universidad Tecnológica de Pereira**, en el marco del Semestre Integrador 2026-2.

Agradecimientos a los docentes que acompañaron el proyecto: _(completar nombres completos)_.

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia incluida en el archivo [`LICENSE`](LICENSE).