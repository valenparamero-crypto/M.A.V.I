# 🤖 M.A.V.I. — Módulo Autónomo de Visión Inteligente

M.A.V.I. es un Vehículo Guiado Automáticamente (AGV) desarrollado como proyecto semestral integrador de Ingeniería Mecatrónica en la Universidad Tecnológica de Pereira. El sistema será capaz de transportar cargas de hasta 1 kg entre estaciones predefinidas de carga y descarga, navegando de forma autónoma en una pista compartida mediante visión artificial y reconocimiento de códigos QR.

---

## 📁 Estructura del Repositorio

```text
M.A.V.I./
├── diseño electrónico/        # Esquemáticos, circuitos y esquemas de conexión
│   └── README.md
├── diseño mecánico/           # Modelado 3D en Fusion 360, ensambles y planos
│   └── README.md
├── documentación/             # Gestión del proyecto, acta de constitución y anexos
│   ├── ACTA DE CONSTITUCIÓN.pdf # Acta oficial formateada bajo norma APA 7ma ed.
│   ├── GANTT.xlsx              # Cronograma de actividades, horas y presupuesto
│   ├── Ruta_Critica_CPM.png    # Diagrama de red de actividades (Método CPM)
│   ├── PLANEACIÓN BITÁCORA SEMANA 8 Y 9.pdf    # Registro de planeación de actividades (Semanas 8-9)
│   └── README.md
├── src/                       # Código fuente principal (Python / ESP32 C++)
│   ├── README.md
│   ├── raspberry/             # Código de la Raspberry Pi 5 (visión, QR, decisiones)
│   │   ├── README.md
│   │   └── i2c_master.py      # Acceso real al bus I2C (pendiente de probar con hardware)
│   ├── esp32/                 # Firmware de la ESP32 (motores, sensores)
│   │   └── README.md
│   └── common/                # Compartido: mapa de registros y protocolo I2C
│       ├── README.md
│       ├── mapa_de_registros.md    # Significado de cada dato compartido entre las tarjetas
│       ├── protocol.py             # Arma y verifica los mensajes según el mapa
│       ├── bus_falso.py            # Simula la ESP32 mientras no hay acceso al hardware
│       └── prueba_protocolo.py     # Prueba que protocol.py y bus_falso.py funcionan juntos
├── .gitignore                 # Archivos excluidos del control de versiones
├── LICENSE                    # Licencia del repositorio
└── README.md                  # Presentación general y estructura del proyecto
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
*Ingeniería Mecatrónica · Formación Integral · Proyecto Integrador I · Proyecto Integrador II*  
Semestre 2026-2