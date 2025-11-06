@echo off
echo ========================================
echo STM32 Programmer Tool - Instalador Simple
echo ========================================
echo.
echo Este instalador descargara e instalara automaticamente
echo todos los componentes necesarios.
echo.
echo Requisitos: Windows 10/11, conexion a internet
echo.

pause

echo.
echo Paso 1: Verificando permisos de administrador...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Permisos OK
) else (
    echo ❌ Necesitas ejecutar como administrador
    echo Clic derecho en este archivo ^> "Ejecutar como administrador"
    pause
    exit /b 1
)

echo.
echo Paso 2: Instalando Python...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile '%TEMP%\python.exe'; Start-Process '%TEMP%\python.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait}"

echo.
echo Paso 3: Instalando OpenOCD...
powershell -Command "& {Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))}"
choco install openocd -y

echo.
echo Paso 4: Verificando instalacion...
python --version
openocd --version

echo.
echo ========================================
echo ✅ INSTALACION COMPLETADA!
echo ========================================
echo.
echo Para usar la herramienta:
echo 1. Conecta tu ST-Link al PC
echo 2. Conecta el STM32 al programador
echo 3. Ejecuta: python src\programmer.py
echo.
echo O usa el ejecutable STM32_Programmer.exe si existe
echo.

pause