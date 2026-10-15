# ⚡ Diseño Electrónico — M.A.V.I.

*Módulo Autónomo de Visión Inteligente*

Esta carpeta contiene la arquitectura electrónica completa, diagramas de bloques, diseño de la placa de circuito impreso (PCB), esquemáticos de conexiones y el registro fotográfico de las pruebas de laboratorio del sistema.

---

## 📁 Estructura del Área

```text
diseño electrónico/
├── Evidencias/                           # Fotografías de banco de pruebas, visión y capturas EDA
│   ├── README.md
│   ├── ajuste_mecanico_acople_rueda.png
│   ├── banco_pruebas_electrónica_esp32.png
│   ├── camara_imx_219_prueba.png
│   ├── chasis_provisional_locomoción_diferencial.png
│   ├── detección_apriltags.png
│   ├── ensamble_ruedas_holonomicas_acoples.png
│   ├── esquema_electronico.png
│   ├── impresion_3d_resina_acoples.png
│   ├── par_motorreductores_ruedas_holonomicas.png
│   ├── reconocimiento_de_pista.png
│   └── render_pcb.png
├── PCB/                                  # Archivos de diseño y fabricación de la PCB
│   └── mavi_pcb_diseno_integral.f3z
├── Diagrama_De_Bloques_Electrónico.png    # Arquitectura e interconexión general de bloques
└── README.md                             # Documentación principal del área
```

---

## 🧩 Componentes y Módulos Principales

* **Unidad de Procesamiento Central:** Raspberry Pi 5 (8GB) para algoritmos de visión artificial, detección de AprilTags y lógica de misión.
* **Control de Bajo Nivel:** Microcontrolador ESP32-S3 para el manejo de actuadores, generación de señales PWM, lecturas de encoder y adquisición de datos de peso.
* **Etapa de Potencia:** Driver TB6612FNG para el control de motorreductores JGY370.
* **Sistema de Visión:** Cámara IMX219-160 (162° FOV) conectada mediante bus flexible CSI.
* **Acondicionamiento y Sensores:** Módulo conversor A/D HX711 acoplado a celda de carga de 5 kg para el sistema de pesaje.
* **Tarjeta Integrada (PCB):** Placa custom diseñada en Autodesk Fusion 360 para consolidar la distribución de alimentación (7.4V / Step-Down 5V), pines de control y conectores de señal.

---

## 👤 Responsables

**Juan Miguel Noreña** — Rol: Líder Técnico / Electrónica  

Formación Integral · Proyecto Integrador I · Proyecto Integrador II · Ingeniería Mecatrónica · Universidad Tecnológica de Pereira · 2026-2