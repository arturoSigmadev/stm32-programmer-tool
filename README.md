# STM32 Programmer Tool

Herramienta simple para programar microcontroladores STM32 usando OpenOCD. Diseñada para facilitar la programación de firmware en entornos de desarrollo y producción.

## 🚀 Instalación Rápida (Recomendado)

### Opción 1: Instalador Automático
**Para usuarios finales - instalación completamente automática**

1. **Descarga** el proyecto desde GitHub
2. **Ejecuta** `INSTALAR.bat` como administrador
3. **Espera** a que se complete la instalación automática
4. **Usa** la herramienta

### Opción 2: Script de PowerShell
**Para usuarios avanzados**

```powershell
# Ejecutar como administrador
.\scripts\install.ps1
```

### Opción 3: Instalación Manual
**Para desarrolladores**

1. Instala Python 3.8+ desde [python.org](https://python.org)
2. Instala OpenOCD:
   - `choco install openocd` (recomendado)
   - O descarga desde [gnutoolchains.com](https://gnutoolchains.com/openocd/)
3. Instala dependencias: `pip install tk`

## 📦 Distribución como Ejecutable

Para crear una versión portable sin instalación:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
python scripts\create_executable.py
```

Esto genera:
- `STM32_Programmer.exe` - Ejecutable standalone
- `STM32_Programmer_Portable.zip` - Paquete completo

## Características

- ✅ Interfaz gráfica simple para seleccionar y programar archivos de firmware
- ✅ Soporte para múltiples controladores STM32 (G4, F1, F4, H7)
- ✅ Integración con OpenOCD para operaciones de bajo nivel
- ✅ Soporte para ST-Link, J-Link y CMSIS-DAP
- ✅ Verificación automática de carga
- ✅ Documentación completa para usuarios finales

## Estructura del Proyecto

```
stm32_programmer_tool/
├── src/
│   └── programmer.py          # Script principal del programador
├── scripts/
│   ├── install.ps1            # Instalador PowerShell avanzado
│   ├── install_dependencies_auto.bat # Instalador automático
│   └── create_executable.py   # Creador de ejecutable
├── docs/
│   ├── manual_usuario.md      # Manual de usuario
│   ├── elementos_necesarios.md # Lista de elementos requeridos
│   └── alternativas_programadores.md # Alternativas de programadores
├── INSTALAR.bat               # Instalador simple (recomendado)
├── README.md                  # Este archivo
└── dist/                      # Archivos de distribución (generados)
```

## Requisitos

- **Python 3.8+** (se instala automáticamente)
- **OpenOCD** (se instala automáticamente)
- **ST-Link V2+** o programador compatible
- **Archivo de firmware** (.hex o .bin)

## Uso

### Desde Ejecutable (Recomendado)
1. Conecta tu programador ST-Link al PC
2. Conecta el STM32 al programador
3. Ejecuta `STM32_Programmer.exe`
4. Selecciona el archivo de firmware
5. Elige el tipo de dispositivo STM32
6. Selecciona el programador
7. Haz clic en "Programar Firmware"

### Desde Código Fuente
```bash
python src/programmer.py
```

## Solución de Problemas

### Error de conexión
- ✅ Verifica conexiones ST-Link
- ✅ Instala drivers desde [ST.com](https://www.st.com/en/development-tools/stsw-link009.html)
- ✅ Prueba con otro cable USB

### Error de dispositivo
- ✅ Verifica alimentación del STM32
- ✅ Comprueba pines SWD/JTAG
- ✅ Selecciona modelo correcto

### Error de archivo
- ✅ Verifica que el firmware sea válido
- ✅ Usa archivos de STM32CubeIDE o similares

## Documentación

Ver carpeta `docs/` para manuales detallados:
- [Manual de Usuario](docs/manual_usuario.md)
- [Elementos Necesarios](docs/elementos_necesarios.md)
- [Alternativas de Programadores](docs/alternativas_programadores.md)

## Soporte

Para soporte técnico, consulta la documentación o contacta al equipo de desarrollo.

---
**STM32 Programmer Tool v1.0**  
*Herramienta de programación para microcontroladores STM32*