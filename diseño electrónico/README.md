<div align="center">

# ⚡ Diseño electrónico

![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?style=for-the-badge&logo=autodesk&logoColor=white)
![ESP32-S3](https://img.shields.io/badge/ESP32--S3-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Raspberry Pi 5](https://img.shields.io/badge/Raspberry%20Pi%205-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white)
![JLCPCB](https://img.shields.io/badge/Fabricado%20en-JLCPCB-1F6FB2?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-Finalizado-2EA44F?style=for-the-badge)

Sistema electrónico de M.A.V.I., integrado en una placa de circuito impreso propia que concentra la distribución de potencia, el control de los motores y la conexión de todos los sensores del vehículo.

<img src="05_Evidencias/pcb_montada_soldada.png" width="70%">

<sub>PCB de M.A.V.I. fabricada y soldada</sub>

</div>

---

### 🧠 Arquitectura

El sistema se organiza en dos niveles de procesamiento que trabajan de forma coordinada:

**Alto nivel — Raspberry Pi 5.** Procesa en tiempo real la imagen de la cámara para identificar la pista, los AprilTags de las estaciones y los obstáculos, y con esa información toma las decisiones de navegación.

**Bajo nivel — ESP32-S3.** Recibe las órdenes de la Raspberry Pi 5 a través del bus I²C, controla la velocidad y el sentido de giro de los motores y lee de forma continua los sensores del vehículo.

---

### 🔋 Distribución de energía

```text
Batería LiPo 7.4 V ──► Interruptor de llave ──┬──► Driver TB6612FNG ──► Motores (7.4 V)
                                              └──► Regulador XL4016 ──► 5.1 V
                                                                         ├──► Raspberry Pi 5
                                                                         ├──► ESP32-S3 ──► 3.3 V para sensores
                                                                         ├──► Lógica del driver
                                                                         └──► Ventilador
```

La batería alimenta directamente a los motores a través del driver, mientras que el regulador reduce el voltaje a 5.1 V para las tarjetas de procesamiento. Los sensores operan a 3.3 V, suministrados por la ESP32-S3.

---

### 🧩 Componentes

#### Procesamiento

**Raspberry Pi 5 (8 GB)** — Computador de placa única encargado de la visión artificial y la toma de decisiones del vehículo.

**ESP32-S3 N16R8** — Microcontrolador de doble núcleo responsable del control de los motores y la lectura de los sensores.

#### Potencia y alimentación

**Batería LiPo 7.4 V · 5000 mAh** — Fuente de energía de todo el sistema.

**Interruptor de llave** — Enciende y apaga el sistema completo. Al requerir una llave, evita encendidos accidentales.

**Regulador XL4016** — Convertidor DC-DC reductor que baja el voltaje de 7.4 V a 5.1 V para la electrónica de control.

**Ventilador 5 V** — Disipa el calor generado por el regulador de voltaje.

#### Actuadores

**Driver TB6612FNG** — Puente H doble que controla la velocidad y el sentido de giro de los dos motores mediante señales PWM de la ESP32-S3.

**Motorreductores JGY-370 con encoder (x2)** — Motores de 6 V y 100 RPM que mueven las ruedas del vehículo. Sus encoders miden el giro de cada rueda para controlar el desplazamiento.

#### Sensores

**Cámara IMX219-160** — Cámara de 8 MP con un campo de visión de 162°, conectada a la Raspberry Pi 5. Captura la pista, los AprilTags y los obstáculos.

**Giroscopio BMI270** — Unidad de medición inercial que registra los giros y las aceleraciones del vehículo.

**Sensor láser VL53L1X** — Sensor de distancia por tiempo de vuelo, con un alcance de hasta 4 m. Mide la distancia a los obstáculos detectados por la cámara.

**Celda de carga 3 kg y módulo HX711** — La celda detecta el peso sobre la plataforma y el HX711 convierte su señal analógica en un valor digital, lo que permite saber si el vehículo transporta carga.

**Par infrarrojo** — Emisor y receptor que permiten el intercambio de señales entre el vehículo y las estaciones de carga y descarga.

#### Seguridad

**Final de carrera** — Interruptor con palanca metálica ubicado en el parachoques. Al producirse un impacto, se activa y detiene los motores de inmediato.

#### Conexión y componentes pasivos

**Borneras de tornillo** — Conectores que aseguran de forma firme los cables de potencia, de la celda de carga y del transmisor infrarrojo.

**Conectores tipo header** — Pines para la conexión de los encoders y los sensores, y de la Raspberry Pi 5 mediante un conector de 40 pines.

**Resistencias de 10 kΩ (x2)** — Ubicadas en la cara inferior de la placa, forman parte del acondicionamiento de las señales del circuito.

**Trimmer** — Potenciómetro de ajuste ubicado junto a la conexión del transmisor infrarrojo.

**Cable plano con conector IDC** — Cable multicolor que comunica la PCB con la Raspberry Pi 5.

**Cable de potencia de silicona** — Cable rojo y negro que conduce la corriente desde la batería hacia el regulador y el driver.

---

### 📂 Contenido de la carpeta

📐 **[01_Diagramas_Conexion](01_Diagramas_Conexion/)** — Árbol de conexiones y tabla de conexiones pin a pin del sistema.

🔌 **[02_Esquematico](02_Esquematico/)** — Esquema eléctrico de la placa en Fusion 360, formato Eagle y PDF.

🟩 **[03_Diseno_PCB](03_Diseno_PCB/)** — Diseño de la placa, modelo 3D e imágenes renderizadas.

🏭 **[04_Fabricacion](04_Fabricacion/)** — Archivos Gerber para fabricación y lista de materiales (BOM).

📷 **[05_Evidencias](05_Evidencias/)** — Registro fotográfico de la placa fabricada.

---

### 📊 Estado del módulo

✅ Diagramas y tabla de conexiones
✅ Esquemático
✅ Diseño de la PCB
✅ Fabricación en JLCPCB
✅ Soldadura y pruebas en el robot

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver al inicio</a></sub>
</div>