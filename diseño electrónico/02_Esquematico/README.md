<div align="center">

# 🔌 Esquemático

![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?style=for-the-badge&logo=autodesk&logoColor=white)
![Eagle](https://img.shields.io/badge/Eagle-1F6FB2?style=for-the-badge)
![PDF](https://img.shields.io/badge/PDF-EC1C24?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

Esquema eléctrico de la PCB de M.A.V.I., que representa con símbolos cada componente del circuito y las conexiones eléctricas entre ellos. Es el punto de partida a partir del cual se diseñó la placa.

</div>

---

### 👁️ Visualización

![PDF](https://img.shields.io/badge/PDF-EC1C24?style=flat-square&logo=adobeacrobatreader&logoColor=white) **MAVI_PCB_ESQUEMATICO.pdf**

Esquema eléctrico completo en una hoja tamaño A3. El circuito está organizado en tres bloques: **CONTROL**, con la ESP32-S3; **CONTROL-POT**, con el driver TB6612FNG, los conectores de los encoders y las borneras de potencia; y **GALGA**, con el módulo HX711 y la conexión de la celda de carga. Incluye también los conectores de la Raspberry Pi 5, el sensor VL53L1X, el BMI270, el transmisor infrarrojo y el pulsador. Permite analizar el funcionamiento del circuito o diagnosticar fallas sin instalar ningún programa, ya que se visualiza directamente en GitHub.

---

### 🛠️ Archivos editables

![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?style=flat-square&logo=autodesk&logoColor=white) **MAVI_PCB_ESQUEMATICO.fsch**

Archivo original del esquemático, creado en Autodesk Fusion 360. Contiene los símbolos de los componentes, sus valores y las conexiones eléctricas del circuito, y está vinculado al diseño de la placa. Es el archivo que se debe utilizar para modificar el circuito o crear una nueva versión. Requiere descarga y se abre con Fusion 360.

![Eagle](https://img.shields.io/badge/Eagle-1F6FB2?style=flat-square) **MAVI_PCB_ESQUEMATICO.sch**

Copia del esquemático exportada al formato de Autodesk Eagle. Su finalidad es que el circuito pueda abrirse en programas distintos a Fusion 360; por ejemplo, KiCad, software gratuito de diseño de circuitos, permite importarlo. Requiere descarga.

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver a Diseño electrónico</a></sub>
</div>