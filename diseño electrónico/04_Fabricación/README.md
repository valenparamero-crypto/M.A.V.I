<div align="center">

# 🏭 Fabricación

![Gerber](https://img.shields.io/badge/Gerber-8250DF?style=for-the-badge)
![CSV](https://img.shields.io/badge/CSV-217346?style=for-the-badge)

Archivos necesarios para la fabricación de la PCB de M.A.V.I. y la adquisición de sus componentes. Con ellos es posible reproducir la placa sin necesidad de abrir el diseño original.

</div>

---

### 📦 Archivos de producción

![Gerber](https://img.shields.io/badge/Gerber-8250DF?style=flat-square) **MAVI_PCB_GERBER.zip**

Paquete comprimido con los archivos Gerber de la placa, el formato estándar que utilizan los fabricantes de circuitos impresos. Cada archivo del paquete describe una capa de la placa: las pistas de cobre, la máscara antisoldante, la serigrafía, el contorno y las perforaciones. Este paquete se envía tal cual al fabricante para producir la PCB. Requiere descarga; su contenido puede revisarse en un visor de Gerber, como los que ofrecen en línea los mismos fabricantes o la herramienta GerbView de KiCad.

![CSV](https://img.shields.io/badge/CSV-217346?style=flat-square) **MAVI_PCB_BOM.csv**

Lista de materiales (BOM, *Bill of Materials*) de la placa. Relaciona cada componente que se monta en la PCB con su referencia, su valor y la cantidad requerida. Sirve para comprar los componentes y como guía durante el ensamble y la soldadura. Se visualiza directamente en GitHub como tabla y también puede abrirse con Excel u otra hoja de cálculo.

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver a Diseño electrónico</a></sub>
</div>