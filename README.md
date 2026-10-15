# 🤖 M.A.V.I. — Módulo Autónomo de Visión Inteligente

## 📌 Descripción del Proyecto

**M.A.V.I.** (*Módulo Autónomo de Visión Inteligente*) es un Vehículo Guiado Automáticamente (AGV) desarrollado como proyecto semestral integrador. El sistema está diseñado para desempeñar tareas de transporte logístico automatizado, capaz de desplazar cargas de hasta **1 kg** de manera autónoma entre estaciones predefinidas de carga y descarga. 

El vehículo navega sobre una pista compartida utilizando un sistema de visión artificial de alta precisión basado en **Raspberry Pi 5** y reconocimiento de **AprilTags**, coordinado en tiempo real con un microcontrolador **ESP32-S3** encargado del control de bajo nivel, actuación de motores y adquisición de sensores.

---

## ⚙️ Arquitectura de Subsistemas y Gestión

El desarrollo de M.A.V.I. se encuentra estructurado en cuatro pilares fundamentales que integran el diseño físico, el software y la rigorosa gestión metodológica del proyecto:

### 1. 🔧 Subsistema Mecánico
* **Chasis y Modelado 3D:** Diseñado paramétricamente en **Autodesk Fusion 360**, optimizando la distribución de masas, el centro de gravedad y la ubicación de la batería (trazabilidad desde versiones en `v1_inicial/` hasta el modelo integral `v2`).
* **Locomoción y Estructura:** Configuración orientada a ruedas **Mecanum** para permitir movilidad omnidireccional en espacios reducidos.
* **Manufactura y Prototipado:** Validación geométrica mediante prototipos en MDF, complementada con fabricación aditiva (SLA/FDM) en resina y polímeros para soportes estructurales de motores y ruedas locas.

### 2. ⚡ Subsistema Electrónico y de Control
* **Tarjeta de Circuito Impreso (PCB):** Placa custom diseñada a la medida en Autodesk Fusion 360 (`mavi_pcb_diseno_integral.f3z`) para consolidar la distribución de potencia (7.4V y regulación Step-Down de 5V) y conectores de señal.
* **Actuación y Potencia:** Driver **TB6612FNG** para el control de velocidad y dirección de los motorreductores **JGY370**.
* **Sensores e Instrumentación:** Incorpora un módulo conversor A/D **HX711** acoplado a una celda de carga de 5 kg para la medición del peso transportado, además de encoders de retroalimentación.

### 3. 💻 Subsistema de Software y Comunicaciones
* **Procesamiento de Alto Nivel (Raspberry Pi 5):** Ejecución de algoritmos en Python para la captura de video mediante la cámara **IMX219** (162° FOV), detección de **AprilTags** y toma de decisiones logísticas.
* **Control de Bajo Nivel (ESP32-S3):** Firmware en C++ (Arduino IDE) encargado de la generación de señales PWM, lectura de encoders y ejecución de órdenes del nivel superior.
* **Capa de Comunicación (I2C):** Arquitectura maestro-esclavo respaldada por un mapa de registros modular (`mapa_de_registros.md`), rutinas de protocolo (`protocol.py`) y entornos de simulación (`bus_falso.py`).

### 4. 📄 Gestión, Planeación y Documentación
* **Formulación y Control:** Respaldado por el *Acta de Constitución* y la *Propuesta Formal* del sistema.
* **Planeación Temporal y de Recursos:** Cronograma detallado en *Gantt.xlsx* y análisis riguroso de la *Ruta Crítica (CPM)* para la optimización de holguras y cumplimiento de hitos.
* **Bitácoras de Trazabilidad:** Registros formales de planeación y ejecución temporal (Semanas 8 a 14), estructurados bajo las normas APA 7ma edición para garantizar la trazabilidad completa del ciclo de desarrollo.

---

## 📁 Estructura Completa del Repositorio

```text
M.A.V.I./
├── diseño electrónico/
│   ├── Evidencias/
│   │   ├── ajuste_mecanico_acople_rueda.png
│   │   ├── banco_pruebas_electrónica_esp32.png
│   │   ├── camara_imx_219_prueba.png
│   │   ├── chasis_provisional_locomoción_diferencial.png
│   │   ├── detección_apriltags.png
│   │   ├── ensamble_ruedas_holonomicas_acoples.png
│   │   ├── esquema_electronico.png
│   │   ├── impresion_3d_resina_acoples.png
│   │   ├── par_motorreductores_ruedas_holonomicas.png
│   │   ├── README.md
│   │   ├── reconocimiento_de_pista.png
│   │   └── render_pcb.png
│   ├── PCB/
│   │   └── mavi_pcb_diseno_integral.f3z
│   ├── Diagrama_De_Bloques_Electrónico.png
│   └── README.md
├── diseño mecánico/
│   ├── CAD/
│   │   ├── v1_inicial/
│   │   │   └── chasis_mavi.stp
│   │   └── chasis_mavi_modelo_integral_v2.step
│   ├── Evidencias/
│   │   ├── chasis_mdf_pruebas_fisicas.png
│   │   ├── proceso_impresion_3d.png
│   │   ├── README.md
│   │   ├── soporte_motores.png
│   │   ├── soportes_rueda_loca_impresos.png
│   │   ├── vista_isometrica_inferior.png
│   │   └── vista_isometrica_superior.png
│   ├── DISEÑO CONCEPTUAL CAD CON LISTADO DE MATERIALES.pdf
│   └── README.md
├── documentación/
│   ├── ACTA DE CONSTITUCIÓN.pdf
│   ├── BITÁCORA DE PLANEACIÓN SEMANA 10 Y 11.pdf
│   ├── BITÁCORA DE PLANEACIÓN SEMANA 12-13-14.pdf
│   ├── GANTT.xlsx
│   ├── PLANEACIÓN BITÁCORA SEMANA 8 Y 9.pdf
│   ├── PLANEACIÓN Y EJECUCIÓN BITÁCORA SEMANA 8 Y 9.pdf
│   ├── PROPUESTA FORMAL.pdf
│   ├── README.md
│   └── Ruta_Critica_CPM.png
├── src/
│   ├── common/
│   │   ├── bus_falso.py
│   │   ├── mapa_de_registros.md
│   │   ├── protocol.py
│   │   ├── prueba_protocolo.py
│   │   └── README.md
│   ├── esp32/
│   │   ├── bascula_hx711.ino
│   │   ├── README.md
│   │   ├── sketch_oct3a.ino
│   │   └── sketch_sep29a_PruebaArranqueMotoresBlutuEncoders.ino
│   ├── raspberry/
│   │   ├── i2c_master.py
│   │   ├── README.md
│   │   └── Test_Coml2C_RBP5-ESP32.py
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

---

## 👥 Equipo de trabajo

| Nombre | Rol |
| :--- | :--- |
| **Juan Miguel Noreña** | Líder Técnico / Electrónica |
| **Sara Edith Perilla** | Mecánica |
| **Edwar Alfonso León** | Programación |
| **Laura Valentina Paramero** | Documentación |

---

## 🏫 Información académica

**Universidad Tecnológica de Pereira — Facultad de Tecnología**  
*Ingeniería Mecatrónica · Formación Integral · Proyecto Integrador I · Proyecto Integrador II · Semestre 2026-2*