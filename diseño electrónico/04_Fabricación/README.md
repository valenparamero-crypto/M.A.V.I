<div align="center">

# 🏭 Fabricación

![Gerber](https://img.shields.io/badge/Gerber-8250DF?style=for-the-badge)
![CSV](https://img.shields.io/badge/CSV-217346?style=for-the-badge)
![JLCPCB](https://img.shields.io/badge/Fabricado%20en-JLCPCB-1F6FB2?style=for-the-badge)

Archivos necesarios para la fabricación de la PCB de M.A.V.I. y la adquisición de sus componentes. Con ellos es posible reproducir la placa sin necesidad de abrir el diseño original.

**Fabricante:** JLCPCB · **Capas:** 2 · **Grosor:** 1.6 mm · **Máscara:** negra · **Dimensiones:** 99.45 × 118.35 mm

</div>

---

### 📦 Archivos de producción

![Gerber](https://img.shields.io/badge/Gerber-8250DF?style=flat-square) **MAVI_PCB_GERBER.zip**

Paquete de producción generado desde Autodesk Fusion 360 y enviado a JLCPCB para la fabricación de la placa. Contiene:

- **Archivos Gerber**, el formato estándar de la industria, con una capa por archivo: cobre superior e inferior, máscara antisoldante, serigrafía, pasta de soldadura y contorno de la placa.
- **Archivo de perforaciones**, que indica la posición y el diámetro de cada agujero.
- **Archivos de ensamble**, con la lista de piezas y la posición de cada componente sobre la placa.
- **Versión en formato ODB++**, alternativa a los Gerber aceptada por muchos fabricantes.

Requiere descarga. Su contenido puede revisarse en un visor de Gerber, como el que ofrece JLCPCB en su plataforma o la herramienta GerbView de KiCad.

![CSV](https://img.shields.io/badge/CSV-217346?style=flat-square) **MAVI_PCB_BOM.csv**

Lista de materiales (BOM, *Bill of Materials*) de la placa. Relaciona cada elemento que se monta en la PCB con su referencia en el diseño, la cantidad, la descripción, el encapsulado y el valor; en los conectores y el pulsador indica además el fabricante y el número de parte. Incluye las tarjetas y módulos (ESP32-S3, driver TB6612FNG y HX711), las borneras de tornillo, los conectores, las dos resistencias de 10 kΩ y el pulsador. Sirve como guía para la compra de componentes, el ensamble y la soldadura. Se abre con Excel u otra hoja de cálculo.

---

<div align="center">
<sub><a href="../README.md">⬅️ Volver a Diseño electrónico</a></sub>
</div>