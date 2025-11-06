# STM32 Programmer Tool - Versión Distribuible

## Instalación Rápida

### Opción 1: Instalador Automático (Recomendado)
1. Ejecuta `scripts/install.ps1` como administrador (PowerShell)
2. O ejecuta `scripts/install_dependencies_auto.bat` como administrador

### Opción 2: Instalación Manual
1. Instala Python 3.8+ desde https://python.org
2. Instala OpenOCD:
   - Usando Chocolatey: `choco install openocd`
   - O descarga desde: https://gnutoolchains.com/openocd/
3. Instala dependencias: `pip install tk`

## Uso

### Ejecutable (Recomendado)
1. Conecta tu programador ST-Link al PC
2. Conecta el STM32 al programador
3. Ejecuta `STM32_Programmer.exe`
4. Selecciona el archivo de firmware (.hex o .bin)
5. Elige el tipo de dispositivo STM32
6. Selecciona el programador (ST-Link, J-Link, CMSIS-DAP)
7. Haz clic en "Programar Firmware"

### Desde Código Fuente
1. Conecta el hardware como arriba
2. Ejecuta: `python src/programmer.py`

## Requisitos de Hardware

- Programador ST-Link V2 o superior
- Cables de conexión (SWD/JTAG)
- Microcontrolador STM32 compatible
- Archivo de firmware (.hex o .bin)

## Solución de Problemas

### Error de conexión
- Verifica que el ST-Link esté conectado correctamente
- Instala los drivers ST-Link desde ST.com
- Prueba con otro cable USB

### Error de dispositivo no reconocido
- Verifica que el STM32 esté alimentado
- Comprueba las conexiones SWD/JTAG
- Selecciona el modelo correcto de STM32

### Error de archivo
- Asegúrate de que el archivo de firmware sea válido
- Verifica que no esté corrupto
- Usa archivos .hex o .bin generados por STM32CubeIDE o similar

## Soporte

Para soporte técnico, contacta al equipo de desarrollo.

---
STM32 Programmer Tool v1.0
Herramienta de programación para microcontroladores STM32
