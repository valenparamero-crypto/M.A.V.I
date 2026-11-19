<div align="center">

# 📐 Diagramas de conexión

![PDF](https://img.shields.io/badge/PDF-EC1C24?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

Documentación que describe cómo se interconectan los componentes electrónicos de M.A.V.I.: desde la batería y el regulador de voltaje hasta cada sensor, actuador y tarjeta de procesamiento.

</div>

---

### 👁️ Visualización

![PDF](https://img.shields.io/badge/PDF-EC1C24?style=flat-square&logo=adobeacrobatreader&logoColor=white) **Arbol_de_conexiones.pdf**

Diagrama de bloques del sistema electrónico, en el que cada componente aparece representado como un bloque y las líneas indican las conexiones de alimentación y de señal entre ellos. Ofrece una visión general de la arquitectura: cómo se distribuye la energía desde la batería, qué elementos se conectan a la Raspberry Pi 5 y cuáles a la ESP32-S3. Se visualiza directamente en GitHub.

![PDF](https://img.shields.io/badge/PDF-EC1C24?style=flat-square&logo=adobeacrobatreader&logoColor=white) **Tabla_de_Conexiones.pdf**

Documento que detalla, pin por pin, la conexión de cada componente del vehículo. Está organizado por módulos (alimentación, driver de motores, encoders, sensores, comunicación I²C, infrarrojo, paro de emergencia y cámara) e indica el pin de origen, el pin de destino y la función de cada conexión. Incluye además un resumen de los pines de la ESP32-S3 en uso y de aquellos que no deben utilizarse. Es la referencia principal para el cableado, el diseño de la PCB y la programación del firmware. Se visualiza directamente en GitHub.

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver a Diseño electrónico</a></sub>
</div>