<div align="center">

# 🤖 M.A.V.I.
### Módulo Autónomo de Visión Inteligente

*Vehículo Guiado Automáticamente (AGV) con plataforma holonómica y visión artificial*

![Raspberry Pi 5](https://img.shields.io/badge/Raspberry%20Pi-5-C51A4A?logo=raspberrypi&logoColor=white)
![ESP32-S3](https://img.shields.io/badge/ESP32--S3-E7352C?logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?logo=cplusplus&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)
![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?logo=autodesk&logoColor=white)
![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)

**Universidad Tecnológica de Pereira** · Facultad de Tecnología
Ingeniería Mecatrónica · Semestre Integrador 2026-2 · **Grupo 2**

[Introducción](#-introducción) ·
[Objetivo](#-objetivo-general) ·
[Áreas](#-áreas-de-desarrollo) ·
[Materiales](#-materiales-y-tecnologías) ·
[Estado](#-estado-actual) ·
[Equipo](#-equipo)

</div>

---

## 📌 Introducción

**M.A.V.I.** es un AGV diseñado para el transporte interno de cargas de hasta **1 kg** entre estaciones de carga y descarga, sobre una pista compartida con otros equipos. El vehículo sigue la pista con una cámara, reconoce cada estación mediante **AprilTags**, detecta si lleva carga, identifica obstáculos y se comunica con las estaciones por infrarrojo. Además, cuenta con una interfaz de usuario para supervisar el vehículo, asignar misiones y detenerlo a distancia.

El proyecto se construye sobre cuatro áreas:

| | Área | En pocas palabras |
| :---: | :--- | :--- |
| 🔧 | **Diseño mecánico** | Chasis impreso en PLA, inspirado en robots logísticos tipo Amazon Kiva, con 2 ruedas Mecanum de tracción diferencial y 4 ruedas locas de apoyo. |
| ⚡ | **Electrónica y potencia** | Batería LiPo de 7.4 V, regulación a 5.1 V con un XL4016 y una PCB propia que integra potencia, driver de motores y sensores. |
| 🎛️ | **Control y movimiento** | Una ESP32-S3 controla los motores con encoders y lee los sensores: IMU, distancia láser, báscula, infrarrojo y paro de emergencia. |
| 👁️ | **Visión por computador** | Una Raspberry Pi 5 con cámara gran angular de 162° detecta la pista, los AprilTags y los obstáculos, y envía las órdenes a la ESP32-S3 por I²C. |

<div align="center">

```text
 Cámara IMX219 ──► Raspberry Pi 5 ──I²C──► ESP32-S3 ──► TB6612FNG ──► Motores JGY-370
  (visión)         (decisiones)           (control)      (driver)       (con encoder)
                                             ▲
               BMI270 · VL53L1X · HX711 · Infrarrojo · Paro de emergencia
```

</div>

---

## 🎯 Objetivo general

Desarrollar un vehículo guiado automáticamente (AGV) que integre una plataforma holonómica y visión artificial, con capacidad para transportar cargas de hasta 1 kg entre estaciones predefinidas de carga y descarga en una pista compartida, antes de finalizar el semestre académico 2026-2.

---

## 📂 Áreas de desarrollo

Cada área tiene su propia carpeta con un README que explica su contenido en detalle.

| Carpeta | Qué contiene |
| :--- | :--- |
| 📄 [**documentación**](documentación/) | Acta de constitución, propuesta formal, cronograma (Gantt), ruta crítica (CPM) y bitácoras de planeación y ejecución. |
| ⚡ [**diseño electrónico**](diseño%20electrónico/) | Diagrama de bloques, esquema electrónico, diseño de la PCB y evidencias de pruebas. |
| 🔧 [**diseño mecánico**](diseño%20mecánico/) | Modelos CAD del chasis (versión inicial y modelo integral), listado de materiales y evidencias de fabricación. |
| 💻 [**src**](src/) | Código fuente: firmware de la ESP32-S3 (C++), programas de la Raspberry Pi 5 (Python) y el protocolo I²C compartido. |

---

## 🧰 Materiales y tecnologías

<details>
<summary><b>⚡ Materiales electrónicos</b> (clic para ver)</summary>
<br>

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Raspberry Pi 5 (8 GB) | Computador de placa única | Visión artificial y toma de decisiones |
| Cámara IMX219-160 | 8 MP, 162° de campo de visión, conexión CSI | Captura de la pista, AprilTags y obstáculos |
| ESP32-S3 N16R8 | Microcontrolador de doble núcleo | Control de motores y lectura de sensores |
| TB6612FNG | Driver de motores (puente H doble) | Controla velocidad y sentido de giro |
| Motorreductor JGY-370 (x2) | 6 V, 100 RPM, con encoder | Tracción y medición del giro de las ruedas |
| Batería LiPo 7.4 V 5000 mAh | Batería de litio-polímero 2S | Alimentación de todo el sistema |
| XL4016 | Convertidor DC-DC reductor | Baja de 7.4 V a 5.1 V para la electrónica |
| BMI270 | Unidad de medición inercial (SPI) | Mide giros y aceleraciones |
| VL53L1X (módulo TOF400C) | Sensor láser de distancia (hasta 4 m) | Mide la distancia a obstáculos |
| Celda de carga 3 kg + HX711 | Sensor de peso y conversor A/D | Detecta si hay carga sobre el vehículo |
| Par infrarrojo | Emisor y receptor IR | Comunicación con las estaciones |
| Pulsador de emergencia | Pulsador normalmente abierto | Detiene los motores ante un riesgo |
| Ventilador 5 V | Ventilador pequeño | Enfría el regulador |
| PCB M.A.V.I. | Placa de circuito impreso propia | Integra potencia y conexiones de señal |

</details>

<details>
<summary><b>🔧 Materiales mecánicos</b> (clic para ver)</summary>
<br>

| Componente | Material | Método de fabricación | Observaciones |
| :--- | :--- | :--- | :--- |
| Chasis final | PLA | Impresión 3D (filamento) | Modelo integral diseñado en Fusion 360 |
| Chasis de pruebas | MDF | Corte láser | Validación de medidas y montaje |
| Soportes de motores | PLA / resina | Impresión 3D | Fijan los motores al chasis |
| Acoples de rueda | Resina | Impresión 3D | Unen el eje del motor con la rueda Mecanum |
| Soportes de ruedas locas | PLA | Impresión 3D | Cuatro puntos de apoyo |
| Ruedas Mecanum 60 mm (x2) | Comercial | Compradas | Rodillos a 45° |
| Ruedas locas (x4) | Comercial | Compradas | Estabilidad del vehículo |

</details>

<details>
<summary><b>🛠️ Herramientas utilizadas</b> (clic para ver)</summary>
<br>

| Herramienta | Tipo | Función principal |
| :--- | :--- | :--- |
| Autodesk Fusion 360 | Software CAD / diseño electrónico | Diseño del chasis, piezas y PCB |
| Arduino IDE | Entorno de programación | Firmware de la ESP32-S3 en C++ |
| Python | Lenguaje de programación | Software de la Raspberry Pi 5 |
| OpenCV | Librería de visión artificial | Detección de pista, AprilTags y obstáculos |
| Visual Studio Code | Editor de código | Desarrollo y conexión remota a la Raspberry Pi 5 |
| Git y GitHub | Control de versiones | Trabajo colaborativo y trazabilidad |
| Impresora 3D | Máquina de fabricación | Chasis y piezas en PLA y resina |
| Cortadora láser | Máquina de fabricación | Piezas de prueba en MDF |
| Microsoft Word | Procesador de texto | Informe, artículo y manual de usuario |
| Microsoft PowerPoint | Presentaciones | Exposiciones del proyecto |
| Microsoft Excel | Hoja de cálculo | Cronograma (Gantt) |

</details>

---

## 📚 Asignaturas relacionadas

| Asignatura | Aporte al proyecto |
| :--- | :--- |
| Programación | Firmware en C++ y software en Python |
| Electrónica analógica y digital | Sensores, lógica de 3.3 V y buses I²C y SPI |
| Electrónica de potencia | Regulación de voltaje y control de motores |
| Inteligencia artificial | Visión por computador para navegación y detección |
| Automatización industrial | Concepto de AGV para logística interna |
| Dibujo técnico | Modelado CAD y planos del chasis |

---

## 🌱 Beneficios esperados

- Mostrar a escala cómo funciona el transporte interno automatizado en manufactura y logística.
- Integrar en un solo prototipo mecánica, electrónica, control, programación y visión artificial.
- Dejar una arquitectura modular (Raspberry Pi 5 + ESP32-S3 por I²C) que otros equipos puedan reutilizar.
- Documentar todo el proceso para que el proyecto pueda replicarse.

---

## 📊 Estado actual

| Módulo | Estado | Detalle |
| :--- | :---: | :--- |
| 🔧 Mecánico | 🟢 Finalizado | Chasis final impreso en PLA y ensamblado con ruedas Mecanum y ruedas locas. |
| ⚡ Electrónico | 🟢 Finalizado | PCB fabricada, soldada y probada en el robot. |
| 🎛️ Control y software | 🟡 En proceso | Las funciones ya se habían probado por separado. Al pasar a la PCB, la comunicación I²C falló; ya se recuperó y se está retomando la integración de todas las funciones y la interfaz de usuario. |
| 📄 Documentación | 🟡 En proceso | Acta, propuesta, Gantt, CPM y bitácoras completas; artículo y manual de usuario en desarrollo. |

<sub>🟢 Finalizado · 🟡 En proceso · 🔴 Pendiente</sub>

---

## 👥 Equipo

| Integrante | Área |
| :--- | :--- |
| **Juan Miguel Noreña** | Líder técnico · Electrónica |
| **Sara Edith Perilla** | Diseño mecánico |
| **Edwar Alfonso León** | Programación |
| **Laura Valentina Paramero** | Documentación |

### Docentes

| Docente | Asignatura |
| :--- | :--- |
| Edward Andrés González Ríos | Proyecto Integrador II |
| Carlos Andrés Rodríguez Pérez | Proyecto Integrador I |
| Angie Tatiana Rengifo Oviedo | Formación Integral |

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más información.

<div align="center">
<sub>Universidad Tecnológica de Pereira · Ingeniería Mecatrónica · 2026</sub>
</div>