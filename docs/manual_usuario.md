# Manual de Usuario - STM32 Programmer Tool

## Introducción

El STM32 Programmer Tool es una herramienta gráfica simple para programar microcontroladores STM32 usando OpenOCD. Está diseñada para facilitar la programación de firmware sin necesidad de conocimientos avanzados de línea de comandos.

## Requisitos del Sistema

### Hardware Necesario
- Computadora con Windows 10/11
- Programador compatible (ST-Link V2/V3, J-Link, CMSIS-DAP)
- Cable USB para conectar el programador
- Microcontrolador STM32 conectado al programador

### Software Necesario
- Python 3.8 o superior
- OpenOCD instalado
- Tkinter (incluido con Python)

## Instalación

1. **Descargar el proyecto:**
   ```
   git clone <url-del-repositorio>
   cd stm32_programmer_tool
   ```

2. **Ejecutar el instalador:**
   ```
   scripts\install_dependencies.bat
   ```

3. **Verificar instalación:**
   - Abrir Command Prompt
   - Ejecutar: `python --version`
   - Ejecutar: `openocd --version`

## Conexión del Hardware

### Paso 1: Conectar el Programador
1. Conectar el programador ST-Link al puerto USB del PC
2. Verificar que Windows reconozca el dispositivo (debería aparecer en Device Manager)

### Paso 2: Conectar el STM32
1. Conectar los pines del programador al STM32:
   - SWDIO → PA13
   - SWCLK → PA14
   - GND → GND
   - VCC → 3.3V (opcional, para alimentación)

### Paso 3: Alimentar el Circuito
- Asegurarse de que el STM32 tenga alimentación (3.3V)
- Si el programador no alimenta el circuito, usar fuente externa

## Uso de la Herramienta

### Inicio de la Aplicación
1. Abrir Command Prompt en la carpeta del proyecto
2. Ejecutar: `python src\programmer.py`
3. Se abrirá la interfaz gráfica

### Programación de Firmware

#### Paso 1: Seleccionar Archivo
1. Hacer clic en "Buscar"
2. Seleccionar el archivo de firmware (.hex o .bin)
3. El nombre del archivo aparecerá en el campo de texto

#### Paso 2: Configurar Dispositivo
1. Seleccionar el tipo de STM32 en "Dispositivo STM32":
   - stm32g4x (para STM32G4)
   - stm32f1x (para STM32F1)
   - stm32f4x (para STM32F4)
   - stm32h7x (para STM32H7)

#### Paso 3: Seleccionar Programador
1. Elegir el tipo de programador en "Tipo de Programador":
   - stlink (ST-Link V2/V3)
   - jlink (Segger J-Link)
   - cmsis-dap (CMSIS-DAP compatible)

#### Paso 4: Programar
1. Hacer clic en "Programar Firmware"
2. Esperar a que aparezca "Programación exitosa"
3. El dispositivo se reiniciará automáticamente

## Solución de Problemas

### Error: "OpenOCD no encontrado"
- Verificar que OpenOCD esté instalado correctamente
- Agregar OpenOCD al PATH del sistema
- Reiniciar Command Prompt

### Error: "No se puede conectar al dispositivo"
- Verificar conexiones físicas (SWDIO, SWCLK, GND)
- Comprobar alimentación del STM32 (3.3V)
- Intentar con otro puerto USB
- Verificar que el STM32 no esté en modo sleep/deep sleep

### Error: "Verificación fallida"
- Verificar que el archivo de firmware sea correcto
- Comprobar que el dispositivo seleccionado coincida con el STM32
- Intentar programar nuevamente

### La aplicación no se abre
- Verificar que Python esté instalado
- Ejecutar: `pip install tk` si Tkinter no está disponible
- Verificar que no haya errores en la consola

## Configuraciones Avanzadas

### Programación con Opciones Personalizadas
Para opciones avanzadas, usar OpenOCD directamente desde línea de comandos:

```bash
# Ejemplo para STM32G4 con ST-Link
openocd -f interface/stlink.cfg -f target/stm32g4x.cfg -c "program firmware.hex verify reset exit"
```

### Archivos de Configuración OpenOCD
Los archivos de configuración están ubicados en:
- `interface/` - Configuraciones de programadores
- `target/` - Configuraciones de dispositivos STM32

## Soporte

Para soporte técnico:
1. Verificar esta documentación
2. Revisar logs de OpenOCD en la consola
3. Consultar la documentación oficial de OpenOCD
4. Contactar al equipo de desarrollo

## Versiones Soportadas

- STM32F1, STM32F4, STM32G4, STM32H7
- Programadores: ST-Link V2/V3, J-Link, CMSIS-DAP
- Sistemas Operativos: Windows 10/11

---

*Última actualización: Octubre 2025*