@echo off
echo ========================================
echo STM32 Programmer Tool - Instalacion
echo ========================================

echo Verificando permisos de administrador...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Ejecutando como administrador
) else (
    echo ❌ Este script requiere permisos de administrador
    echo Por favor, ejecuta como administrador
    pause
    exit /b 1
)

echo.
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no esta instalado.
    echo Descargando e instalando Python 3.11...

    REM Descargar Python
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"

    if not exist "%TEMP%\python-installer.exe" (
        echo ❌ Error al descargar Python
        echo Descargalo manualmente desde: https://python.org
        pause
        exit /b 1
    )

    echo Instalando Python...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    REM Verificar instalación
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar Python
        pause
        exit /b 1
    )

    echo ✅ Python instalado correctamente
) else (
    echo ✅ Python ya esta instalado
)

echo.
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias Python...
pip install tk

echo.
echo Verificando OpenOCD...
openocd --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ OpenOCD no esta instalado.
    echo Instalando OpenOCD usando Chocolatey...

    REM Verificar si Chocolatey esta instalado
    choco --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Instalando Chocolatey...
        powershell -Command "& {Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))}"
    )

    echo Instalando OpenOCD...
    choco install openocd -y

    REM Verificar instalación
    openocd --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar OpenOCD con Chocolatey
        echo.
        echo Opciones alternativas:
        echo 1. Descargar desde: https://gnutoolchains.com/openocd/
        echo 2. Instalar desde fuente: git clone https://git.code.sf.net/p/openocd/code openocd-code
        echo.
        pause
        exit /b 1
    )

    echo ✅ OpenOCD instalado correctamente
) else (
    echo ✅ OpenOCD ya esta instalado
)

echo.
echo Verificando drivers ST-Link...
REM Verificar si ST-Link esta conectado
st-info --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ℹ️  ST-Link drivers no encontrados o no hay dispositivo conectado
    echo ℹ️  Si tienes un ST-Link conectado, instala los drivers desde:
    echo ℹ️  https://www.st.com/en/development-tools/stsw-link009.html
)

echo.
echo ========================================
echo ✅ Instalacion completada exitosamente!
echo ========================================
echo.
echo Para usar la herramienta:
echo 1. Conecta tu programador ST-Link al PC
echo 2. Conecta el STM32 al programador
echo 3. Ejecuta: python src\programmer.py
echo.
echo O crea un acceso directo al archivo src\programmer.py
echo.
pause