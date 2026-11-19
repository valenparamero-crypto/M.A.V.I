<div align="center">

# ⚡ Diseño electrónico — M.A.V.I.

*Distribución de potencia, control de motores e integración de sensores*

![Estado](https://img.shields.io/badge/Estado-Finalizado-brightgreen)
![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?logo=autodesk&logoColor=white)
![ESP32-S3](https://img.shields.io/badge/ESP32--S3-E7352C?logo=espressif&logoColor=white)
![Raspberry Pi 5](https://img.shields.io/badge/Raspberry%20Pi-5-C51A4A?logo=raspberrypi&logoColor=white)

<img src="03_Diseno_PCB/MAVI_PCB_3D_SUPERIOR.png" width="45%">
&nbsp;
<img src="03_Diseno_PCB/MAVI_PCB_3D_INFERIOR.png" width="45%">

<sub>Modelo 3D de la PCB — vista superior e inferior</sub>

</div>

---

## 📌 Descripción

El sistema electrónico de M.A.V.I. se integra en una **PCB propia** diseñada en Autodesk Fusion 360. La placa concentra la distribución de potencia, el driver de los motores y los conectores de todos los sensores, lo que reemplaza el cableado en protoboard por una conexión ordenada y confiable.

La arquitectura se divide en dos niveles:
- **Alto nivel — Raspberry Pi 5:** procesa la imagen de la cámara y toma las decisiones de navegación.
- **Bajo nivel — ESP32-S3:** controla los motores y lee los sensores. Recibe las órdenes de la Raspberry Pi 5 por I²C.

### Distribución de energía

```text
Batería LiPo 7.4 V ──► Interruptor de llave ──┬──► Driver TB6612FNG ──► Motores (7.4 V)
                                              └──► Regulador XL4016 ──► 5.1 V
                                                                         ├──► Raspberry Pi 5
                                                                         ├──► ESP32-S3 ──► 3.3 V para sensores
                                                                         ├──► Lógica del driver
                                                                         └──► Ventilador
```

---

## 🧩 Componentes electrónicos

### Procesamiento

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Raspberry Pi 5 (8 GB) | Computador de placa única | Visión artificial y toma de decisiones |
| ESP32-S3 N16R8 | Microcontrolador de doble núcleo | Control de motores y lectura de sensores |

### Potencia y alimentación

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Batería LiPo 7.4 V 5000 mAh | Batería de litio-polímero 2S | Alimentación de todo el sistema |
| Interruptor de llave | Interruptor ON/OFF con llave | Enciende y apaga todo el sistema |
| Regulador XL4016 | Convertidor DC-DC reductor | Baja el voltaje de 7.4 V a 5.1 V |
| Ventilador 5 V | Ventilador pequeño | Enfría el regulador |

### Actuadores

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Driver TB6612FNG | Puente H doble | Controla velocidad y sentido de giro de los motores |
| Motorreductor JGY-370 (x2) | Motor 6 V, 100 RPM, con encoder | Mueve las ruedas y mide su giro |

### Sensores

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Cámara IMX219-160 | 8 MP, 162° de campo de visión, conexión CSI | Captura de la pista, AprilTags y obstáculos |
| Giroscopio BMI270 | Unidad de medición inercial (SPI) | Mide giros y aceleraciones del vehículo |
| Sensor láser VL53L1X | Sensor de distancia por tiempo de vuelo, hasta 4 m | Mide la distancia a obstáculos |
| Celda de carga 3 kg | Galga extensiométrica | Detecta el peso sobre el vehículo |
| Módulo HX711 | Conversor analógico-digital de 24 bits | Convierte la señal de la celda de carga |
| Par infrarrojo | Emisor y receptor IR | Comunicación con las estaciones |

### Seguridad

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| Sensor de impacto (bumper) | Interruptor ubicado en el parachoques | Detiene los motores de inmediato si el vehículo choca |

### Componentes pasivos y conexión

| Componente | Descripción | Función |
| :--- | :--- | :--- |
| PCB M.A.V.I. | Placa de circuito impreso propia | Integra potencia y señales en una sola tarjeta |
| Borneras de tornillo | Conectores de 2 terminales | Conexión firme de cables de potencia y sensores |
| Conectores tipo header | Pines macho y hembra | Conexión de módulos, encoders y sensores |
| Trimmer _(confirmar valor)_ | Potenciómetro de ajuste | _(confirmar función)_ |
| Resistencia _(confirmar valor)_ | Resistencia de carbón | _(confirmar función)_ |
| Cable plano (cable cinta) con conector IDC | Cable multicolor | Conexión entre la PCB y la Raspberry Pi 5 |
| Cable de potencia de silicona | Cable rojo y negro, calibre _(confirmar)_ AWG | Lleva la corriente de la batería al regulador y al driver |

La lista completa de componentes de la placa está en el archivo [BOM](04_Fabricacion/MAVI_PCB_BOM.csv), y la conexión pin a pin en la [Tabla de conexiones](01_Diagramas_Conexion/Tabla_de_Conexiones.pdf).

---

## 📂 Contenido de la carpeta

| Carpeta | Archivos | Para qué sirve |
| :--- | :--- | :--- |
| 📐 [01_Diagramas_Conexion](01_Diagramas_Conexion/) | Árbol de conexiones · Tabla de conexiones | Muestran qué se conecta con qué y en qué pin |
| 🔌 [02_Esquematico](02_Esquematico/) | `.fsch` (Fusion) · `.sch` (Eagle) · `.pdf` | Esquema eléctrico de la placa |
| 🟩 [03_Diseno_PCB](03_Diseno_PCB/) | `.fbrd` (Fusion) · `.brd` (Eagle) · `.pdf` · modelo 3D `.step` · imágenes 3D | Diseño de la placa y su modelo 3D |
| 🏭 [04_Fabricacion](04_Fabricacion/) | Gerber `.zip` · BOM `.csv` | Archivos para fabricar la PCB y lista de componentes |
| 📷 [05_Evidencias](05_Evidencias/) | Fotografías | Registro de la PCB soldada |

> 💡 Los archivos `.pdf` se pueden ver directamente en GitHub sin instalar ningún programa.

---

## 📷 La placa real

<div align="center">
<img src="05_Evidencias/pcb_montada_soldada.png" width="70%">
</div>

---

## 📊 Estado

| Etapa | Estado |
| :--- | :---: |
| Diagramas y tabla de conexiones | 🟢 |
| Esquemático | 🟢 |
| Diseño de la PCB | 🟢 |
| Fabricación | 🟢 |
| Soldadura y pruebas en el robot | 🟢 |

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver al inicio</a></sub>
</div>