# Elementos Necesarios para Programar STM32

## Lista de Componentes y Herramientas

### 1. Hardware Obligatorio

#### Programador/Debug
- **ST-Link V2 o V3** (recomendado)
  - Precio: ~$20-50 USD
  - Compatible con todos los STM32
  - Soporte oficial de STMicroelectronics
- **Alternativas:**
  - Segger J-Link (~$300-500 USD)
  - CMSIS-DAP compatible (~$10-30 USD)

#### Cables y Conectores
- **Cable USB A a Mini-B** (para ST-Link)
- **Dupont cables macho-hembra** (para conexiones SWD)
  - 4 cables: SWDIO, SWCLK, GND, VCC (opcional)
- **Pin header** (para conectar al STM32)

#### Alimentación
- **Fuente de 3.3V** (si el programador no alimenta)
- **Multímetro** (para verificar voltajes)

### 2. Software Obligatorio

#### Sistema Operativo
- **Windows 10/11** (nativo)
- **Linux** (Ubuntu recomendado)
- **macOS** (con Homebrew)

#### Python
- **Python 3.8+**
- **Tkinter** (incluido con Python)
- **Pip** (para instalar dependencias)

#### OpenOCD
- **Versión 0.11+**
- **Archivos de configuración** para STM32
- **Drivers** para el programador

### 3. Archivos de Firmware

#### Formatos Soportados
- **.hex** (Intel HEX) - Recomendado
- **.bin** (binario crudo)
- **.elf** (para debugging)

#### Herramientas para Generar Firmware
- **STM32CubeIDE** (gratuito)
- **Keil MDK**
- **IAR Embedded Workbench**
- **GCC + Makefile**

### 4. Conexiones Físicas

#### Pines SWD Obligatorios
```
STM32    ←→   Programador
PA13     ←→   SWDIO
PA14     ←→   SWCLK
GND      ←→   GND
```

#### Pines Opcionales
```
STM32    ←→   Programador
3.3V     ←→   VCC (alimentación)
NRST     ←→   RESET (reinicio)
```

### 5. Configuración del Entorno

#### Variables de Entorno (Windows)
```cmd
set PATH=%PATH%;"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin"
set PATH=%PATH%;"C:\OpenOCD\bin"
```

#### Verificación de Instalación
```bash
# Verificar Python
python --version

# Verificar OpenOCD
openocd --version

# Verificar Tkinter
python -c "import tkinter; print('Tkinter OK')"
```

### 6. Requisitos del Circuito STM32

#### Alimentación Estable
- **3.3V ±0.1V**
- **Corriente mínima:** 50mA
- **Filtro de ruido:** Capacitor 10µF + 0.1µF

#### Oscilador
- **HSE:** Cristal de 8MHz (para precisión)
- **LSI:** Oscilador interno (suficiente para desarrollo)

#### Protección
- **Diodos de protección** en pines de entrada
- **Resistencias pull-up/down** según datasheet
- **Reset externo** (botón de reset)

### 7. Herramientas de Verificación

#### Software
- **STM32CubeProgrammer** (para verificar programación)
- **Terminal serie** (PuTTY, minicom)
- **Analizador lógico** (opcional)

#### Hardware de Verificación
- **LED de estado** conectado a GPIO
- **Botón de reset**
- **Puerto serie** (para debug)

### 8. Costos Estimados

#### Configuración Básica (~$50-100)
- ST-Link V2: $25
- Cables Dupont: $5
- Protoboard: $5
- Capacitores/resistores: $10
- STM32 Nucleo board: $15 (incluye programador)

#### Configuración Profesional (~$200-500)
- ST-Link V3: $50
- Osciloscopio básico: $100
- Analizador lógico: $50
- STM32 Discovery kit: $100

### 9. Checklist Pre-Programación

- [ ] Programador conectado y reconocido por Windows
- [ ] Conexiones SWD correctas (PA13, PA14, GND)
- [ ] Alimentación 3.3V estable en STM32
- [ ] Archivo de firmware válido (.hex)
- [ ] OpenOCD instalado y en PATH
- [ ] Python con Tkinter funcionando
- [ ] STM32 no en modo deep sleep/bootloader

### 10. Troubleshooting Hardware

#### Problema: "No device found"
- Verificar conexiones físicas
- Comprobar alimentación
- Intentar otro puerto USB
- Verificar drivers del programador

#### Problema: "Verification failed"
- Comprobar formato del archivo firmware
- Verificar dirección de memoria correcta
- Intentar programar sin verificación primero

#### Problema: "Target voltage too low"
- Verificar alimentación 3.3V
- Comprobar cables de alimentación
- Usar fuente externa si es necesario

---

*Esta lista cubre los elementos esenciales para programar STM32 de manera confiable. Para proyectos específicos, pueden requerirse componentes adicionales.*