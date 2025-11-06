# Guía de Instalación - STM32 Programmer Tool

## Para Clientes - Instalación Sencilla

### 🎯 Opción Más Fácil: Instalador Automático

1. **Descarga** el proyecto desde GitHub o recibe el ZIP del desarrollador
2. **Busca** el archivo `INSTALAR.bat` en la raíz del proyecto
3. **Clic derecho** en `INSTALAR.bat` → **"Ejecutar como administrador"**
4. **Espera** 2-3 minutos mientras se instala todo automáticamente
5. **¡Listo!** La herramienta está instalada y lista para usar

**¿Qué instala automáticamente?**
- ✅ Python 3.11 (lenguaje de programación)
- ✅ OpenOCD (herramienta de programación STM32)
- ✅ Todas las dependencias necesarias
- ✅ Verificación de instalación

### 💻 Opción Profesional: Ejecutable Portable

Si prefieres no instalar nada en el sistema:

1. **Pide** al desarrollador el archivo `STM32_Programmer_Portable.zip`
2. **Extrae** el ZIP en cualquier carpeta
3. **Ejecuta** `STM32_Programmer.exe`
4. **¡Listo!** No requiere instalación

**Ventajas:**
- ✅ No modifica el sistema operativo
- ✅ Funciona desde USB o cualquier carpeta
- ✅ No requiere permisos de administrador

## Verificación de Instalación

Después de instalar, verifica que todo funciona:

1. **Conecta** tu programador ST-Link al PC
2. **Conecta** el STM32 al programador
3. **Ejecuta** la herramienta:
   - Desde código: `python src/programmer.py`
   - Desde ejecutable: `STM32_Programmer.exe`
4. **Selecciona** un archivo de firmware (.hex o .bin)
5. **Elige** el tipo de STM32
6. **Haz clic** en "Programar Firmware"

## Solución de Problemas Comunes

### ❌ "No tengo permisos de administrador"
**Solución:** Clic derecho en el instalador → "Ejecutar como administrador"

### ❌ "Error de conexión al dispositivo"
**Solución:**
- Verifica que el ST-Link esté conectado
- Instala drivers desde: https://www.st.com/en/development-tools/stsw-link009.html
- Prueba con otro cable USB

### ❌ "Python no se instaló"
**Solución:** Descarga manualmente desde https://python.org e instala

### ❌ "OpenOCD no funciona"
**Solución:** Ejecuta `choco install openocd` en PowerShell como administrador

## Requisitos Mínimos

- **Sistema Operativo:** Windows 10 o superior
- **Espacio en disco:** 500 MB libres
- **Conexión a internet:** Solo para instalación (opcional después)
- **Hardware:** ST-Link V2+ y microcontrolador STM32

## Contacto

Si tienes problemas con la instalación, contacta al equipo de desarrollo con:
- Versión de Windows
- Mensaje de error exacto
- Paso donde falló la instalación

---
**Documentación preparada para distribución al cliente**