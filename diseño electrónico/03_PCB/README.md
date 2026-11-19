<div align="center">

# 🟩 Diseño de la PCB

![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?style=for-the-badge&logo=autodesk&logoColor=white)
![Eagle](https://img.shields.io/badge/Eagle-1F6FB2?style=for-the-badge)
![STEP](https://img.shields.io/badge/STEP-6E7781?style=for-the-badge)
![PDF](https://img.shields.io/badge/PDF-EC1C24?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

Placa de circuito impreso propia de M.A.V.I., que integra en una sola tarjeta la distribución de potencia, el control de los motores y la conexión de los sensores.

<img src="MAVI_PCB_3D_SUPERIOR.png" width="42%">
&nbsp;&nbsp;
<img src="MAVI_PCB_3D_INFERIOR.png" width="42%">

<sub>Vista superior e inferior del modelo 3D</sub>

</div>

---

### 👁️ Visualización

![PDF](https://img.shields.io/badge/PDF-EC1C24?style=flat-square&logo=adobeacrobatreader&logoColor=white) **MAVI_PCB_DISENO.pdf**

Plano completo de la placa, en el que se observan las pistas de cobre que conectan los componentes, la ubicación de cada elemento y las serigrafías que identifican borneras y conectores. Es el documento de referencia para revisar el diseño, verificar conexiones o guiar el proceso de soldadura, sin necesidad de instalar ningún programa, ya que se visualiza directamente en GitHub.

![PNG](https://img.shields.io/badge/PNG-2EA44F?style=flat-square) **MAVI_PCB_3D_SUPERIOR.png** · **MAVI_PCB_3D_INFERIOR.png**

Imágenes renderizadas del modelo 3D de la placa, por la cara superior y la inferior. Muestran cómo luce la PCB con sus componentes montados, lo que permite reconocer la disposición de los módulos (ESP32-S3, driver de motores, sensores y borneras) antes de tener la placa física. Se visualizan directamente en GitHub.

---

### 🛠️ Archivos editables

![Fusion 360](https://img.shields.io/badge/Fusion%20360-FF6A00?style=flat-square&logo=autodesk&logoColor=white) **MAVI_PCB_DISENO.fbrd**

Archivo original del diseño de la placa, creado en Autodesk Fusion 360. Contiene toda la información editable: el trazado de las pistas, las capas de cobre, la posición de los componentes y las reglas de diseño. Es el archivo que se debe utilizar para realizar cualquier modificación o una nueva versión de la placa. Requiere descarga y se abre con Fusion 360.

![Eagle](https://img.shields.io/badge/Eagle-1F6FB2?style=flat-square) **MAVI_PCB_DISENO.brd**

Copia del diseño de la placa exportada al formato de Autodesk Eagle, uno de los formatos más utilizados en diseño electrónico. Su finalidad es que el diseño pueda abrirse en programas distintos a Fusion 360; por ejemplo, KiCad, software gratuito de diseño de circuitos, permite importarlo. Requiere descarga.

![STEP](https://img.shields.io/badge/STEP-6E7781?style=flat-square) **MAVI_PCB_3D.step**

Modelo tridimensional de la placa en formato STEP, el estándar para intercambiar modelos entre programas CAD. Conserva las dimensiones reales de la PCB y sus componentes, por lo que se utiliza para integrarla en el ensamble mecánico del vehículo y verificar que encaje correctamente en el chasis. Requiere descarga y se abre con Fusion 360, FreeCAD u otro software CAD.

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver a Diseño electrónico</a></sub>
</div>