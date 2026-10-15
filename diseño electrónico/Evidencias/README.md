# 📸 Galería de Evidencias — Diseño Electrónico

*Registro técnico de pruebas de laboratorio, prototipado físico, visión artificial, diseño de PCB y arquitectura del sistema de M.A.V.I.*

---

## 🧪 Pruebas de Laboratorio y Prototipado Físico
> **Responsables:** Juan Miguel Noreña (Líder Técnico / Electrónica)

### 1. ⚡ Banco de Pruebas Electrónico
> **Componentes:** ESP32-S3 · Driver TB6612FNG · Fuente de alimentación (5.1V @ 2A)

![Banco de pruebas electrónica](banco_pruebas_electrónica_esp32.png)

*Montaje de laboratorio para la validación de señales PWM, protocolo de comunicación y comportamiento térmico del driver de potencia.*

### 2. 🖨️ Fabricación de Acoples en Resina (SLA)
> **Proceso:** Impresión 3D en resina fotopolimérica / Curado UV

![Impresión 3D de acoples](impresion_3d_resina_acoples.png)

*Prototipado rápido de adaptadores a medida para la interfaz entre los ejes de los motorreductores y las ruedas Mecanum.*

### 3. 🛠️ Ajuste Mecánico de Tolerancias
> **Herramienta:** Dremel / Mototool de precisión

![Ajuste mecánico de acoples](ajuste_mecanico_acople_rueda.png)

*Rectificado de tolerancia dimensional en el acople impreso para garantizar concentricidad y minimizar holgura mecánica.*

### 4. ⚙️ Adaptadores y Ruedas Mecanum
> **Componentes:** Ruedas omnidireccionales + Acoples impresos

![Ensamble de ruedas y acoples](ensamble_ruedas_holonomicas_acoples.png)

*Integración física de las ruedas Mecanum con los adaptadores terminados antes de su montaje en los motores.*

### 5. 🔍 Par de Motorreductores y Tracción
> **Vista:** Superior / Simetría de actuadores

![Par de motorreductores](par_motorreductores_ruedas_holonomicas.png)

*Vista superior de la alineación y simetría del par de motorreductores ensamblados con sus respectivas ruedas de prueba.*

### 6. 🚚 Chasis Provisional de Locomoción
> **Estructura:** Base provisional de madera · Montaje de tracción diferencial

![Chasis provisional montado](chasis_provisional_locomoción_diferencial.png)

*Estructura provisional ensamblada para la ejecución de pruebas dinámicas de trayectoria, viraje y compensación de velocidad por software.*

---

## 📷 Pruebas de Visión Artificial y Sensores
> **Responsables:** Equipo M.A.V.I. (Integración RPi5 + IMX219)

### 7. 📹 Validación de Cámara IMX219
> **Hardware:** Raspberry Pi 5 · Cámara IMX219-160 (162° FOV)

![Prueba Cámara IMX219](camara_imx_219_prueba.png)

*Verificación de adquisición de flujo de video en tiempo real, calibración de contraste y ángulo de visión de la cámara instalada.*

### 8. 🏷️ Detección y Lectura de AprilTags
> **Algoritmo:** OpenCV / AprilTag Library

![Detección de AprilTags](detección_apriltags.png)

*Validación del algoritmo de procesamiento de imagen para el reconocimiento, identificación de IDs y estimación de pose a partir de AprilTags.*

### 9. 🏁 Reconocimiento de Pista y Entorno
> **Procesamiento:** Visión por computador en Raspberry Pi 5

![Reconocimiento de Pista](reconocimiento_de_pista.png)

*Pruebas de adquisición de imagen del entorno de navegación y segmentación de la pista de pruebas para la guía del robot.*

---

## 💻 Arquitectura Electrónica, Esquemático y Diseño de PCB
> **Responsable:** Sara Edith Perilla (Mecánica / Integración Electrónica)

### 10. 📐 Esquemático Electrónico Consolidado
> **Herramienta:** Autodesk Fusion Electronics / Schematics

![Esquema Electrónico](esquema_electronico.png)

*Diagrama esquemático consolidado del sistema que integra microcontroladores (ESP32-S3), módulo de procesamiento (Raspberry Pi 5), reguladores de voltaje, etapas de potencia (TB6612FNG) y acondicionado de señal para sensores.*

### 11. 🎛️ Diseño y Render de PCB (Placa de Circuito Impreso)
> **Archivo Integrado:** `mavi_pcb_diseno_integral.f3z` en `/PCB/`

![Render PCB](render_pcb.png)

*Vista integral en Autodesk Fusion 360 del esquema, trazado de pistas (layout 2D) y renderizado 3D de la tarjeta de circuito impreso proyectada para la versión consolidada del MVP.*

---

[⬅️ Volver a Diseño Electrónico](../README.md)