# STM32 Programmer Tool

Herramienta simple para programar microcontroladores STM32 usando OpenOCD. Diseñada para facilitar la programación de firmware en entornos de desarrollo y producción.

## Características

- Interfaz gráfica simple para seleccionar y programar archivos de firmware
- Soporte para múltiples controladores STM32
- Integración con OpenOCD para operaciones de bajo nivel
- Documentación básica para usuarios finales

## Estructura del Proyecto

```
stm32_programmer_tool/
├── src/
│   └── programmer.py          # Script principal del programador
├── docs/
│   ├── manual_usuario.md      # Manual de usuario
│   ├── elementos_necesarios.md # Lista de elementos requeridos
│   └── alternativas_programadores.md # Alternativas de programadores
├── scripts/
│   └── install_dependencies.bat # Script de instalación
└── README.md                  # Este archivo
```

## Requisitos

- Python 3.8+
- OpenOCD instalado
- Controlador ST-Link o compatible
- Archivo de firmware (.hex o .bin)

## Instalación

1. Ejecutar `scripts/install_dependencies.bat`
2. Verificar instalación de OpenOCD
3. Conectar el programador ST-Link al PC y al STM32

## Uso

Ejecutar `python src/programmer.py` y seguir las instrucciones en pantalla.

## Documentación

Ver carpeta `docs/` para manuales detallados.