# 📸 Galería de Evidencias — Diseño Electrónico

*Registro técnico de pruebas de laboratorio, prototipado físico, selección de herramientas EDA y desarrollo del esquemático de M.A.V.I.*

---

## 🧪 Pruebas de Laboratorio y Prototipado Físico
> **Responsable:** Juan Miguel Noreña (Líder Técnico / Electrónica)

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

## 💻 Arquitectura EDA, Librerías 3D y Esquemático
> **Responsable:** Sara Edith Perilla (Mecánica / Apoyo de Integración Electrónica)

### 7. 📐 Evaluación EDA y Creación de Librerías Electrónicas
> **Herramienta:** Autodesk Fusion Electronics / Schematics

![Esquema preliminar en Fusion](esquema_preliminar_fusion.png)

*Evaluación comparativa de plataformas EDA (Fritzing, KiCad, EasyEDA) e integración directa en Autodesk Fusion 360. Desarrollo desde cero de las librerías electrónicas (símbolos esquemáticos, huellas y modelos 3D) para la **Raspberry Pi 5**, **ESP32-S3** y driver **TB6612FNG**, permitiendo estructurar el esquemático preliminar y garantizar la co-integración 3D con el chasis.*

---

[⬅️ Volver a Diseño Electrónico](../README.md)