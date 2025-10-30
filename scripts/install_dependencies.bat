@echo off
echo ========================================
echo STM32 Programmer Tool - Instalacion
echo ========================================

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado. Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo Instalando dependencias Python...
pip install tk

echo.
echo Verificando OpenOCD...
openocd --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo OpenOCD no esta instalado.
    echo Opciones de instalacion:
    echo 1. Usando Chocolatey: choco install openocd
    echo 2. Descargar desde: https://gnutoolchains.com/openocd/
    echo 3. Instalar desde fuente: git clone https://git.code.sf.net/p/openocd/code openocd-code
    echo.
    echo Una vez instalado OpenOCD, ejecuta este script nuevamente.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacion completada exitosamente!
echo ========================================
echo.
echo Para usar la herramienta:
echo 1. Conecta tu programador ST-Link al PC
echo 2. Conecta el STM32 al programador
echo 3. Ejecuta: python src\programmer.py
echo.
pause