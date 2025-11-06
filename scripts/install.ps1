# STM32 Programmer Tool - Instalador Automático
# Ejecutar como administrador

param(
    [switch]$Force,
    [switch]$SkipDrivers
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "STM32 Programmer Tool - Instalador" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verificar permisos de administrador
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Write-Host "❌ Este script requiere permisos de administrador" -ForegroundColor Red
    Write-Host "Por favor, ejecuta PowerShell como administrador y vuelve a intentar" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✅ Ejecutando como administrador" -ForegroundColor Green

# Función para verificar si un comando existe
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Instalar Python si no está instalado
Write-Host "`nVerificando Python..." -ForegroundColor Yellow
if (-not (Test-Command python)) {
    Write-Host "❌ Python no está instalado." -ForegroundColor Red
    Write-Host "Descargando e instalando Python 3.11..." -ForegroundColor Yellow

    $pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"

    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "Instalando Python..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait

        # Verificar instalación
        if (Test-Command python) {
            Write-Host "✅ Python instalado correctamente" -ForegroundColor Green
        } else {
            throw "Python no se instaló correctamente"
        }
    } catch {
        Write-Host "❌ Error al instalar Python: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Descárgalo manualmente desde: https://python.org" -ForegroundColor Yellow
        Read-Host "Presiona Enter para salir"
        exit 1
    }
} else {
    Write-Host "✅ Python ya está instalado" -ForegroundColor Green
}

# Actualizar pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    Write-Host "✅ Pip actualizado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ No se pudo actualizar pip, continuando..." -ForegroundColor Yellow
}

# Instalar dependencias Python
Write-Host "`nInstalando dependencias Python..." -ForegroundColor Yellow
try {
    pip install tk
    Write-Host "✅ Dependencias Python instaladas" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al instalar dependencias Python" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Instalar OpenOCD
Write-Host "`nVerificando OpenOCD..." -ForegroundColor Yellow
if (-not (Test-Command openocd)) {
    Write-Host "❌ OpenOCD no está instalado." -ForegroundColor Red
    Write-Host "Instalando OpenOCD usando Chocolatey..." -ForegroundColor Yellow

    # Instalar Chocolatey si no está instalado
    if (-not (Test-Command choco)) {
        Write-Host "Instalando Chocolatey..." -ForegroundColor Yellow
        try {
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
            Write-Host "✅ Chocolatey instalado" -ForegroundColor Green
        } catch {
            Write-Host "❌ Error al instalar Chocolatey" -ForegroundColor Red
            Read-Host "Presiona Enter para salir"
            exit 1
        }
    }

    # Instalar OpenOCD
    try {
        choco install openocd -y
        if (Test-Command openocd) {
            Write-Host "✅ OpenOCD instalado correctamente" -ForegroundColor Green
        } else {
            throw "OpenOCD no se instaló correctamente"
        }
    } catch {
        Write-Host "❌ Error al instalar OpenOCD con Chocolatey" -ForegroundColor Red
        Write-Host "`nOpciones alternativas:" -ForegroundColor Yellow
        Write-Host "1. Descargar desde: https://gnutoolchains.com/openocd/" -ForegroundColor Yellow
        Write-Host "2. Instalar desde fuente: git clone https://git.code.sf.net/p/openocd/code openocd-code" -ForegroundColor Yellow
        Read-Host "Presiona Enter para salir"
        exit 1
    }
} else {
    Write-Host "✅ OpenOCD ya está instalado" -ForegroundColor Green
}

# Verificar drivers ST-Link (opcional)
if (-not $SkipDrivers) {
    Write-Host "`nVerificando drivers ST-Link..." -ForegroundColor Yellow
    if (-not (Test-Command st-info)) {
        Write-Host "ℹ️ ST-Link drivers no encontrados o no hay dispositivo conectado" -ForegroundColor Yellow
        Write-Host "ℹ️ Si tienes un ST-Link conectado, instala los drivers desde:" -ForegroundColor Yellow
        Write-Host "ℹ️ https://www.st.com/en/development-tools/stsw-link009.html" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Drivers ST-Link encontrados" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ Instalación completada exitosamente!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nPara usar la herramienta:" -ForegroundColor White
Write-Host "1. Conecta tu programador ST-Link al PC" -ForegroundColor White
Write-Host "2. Conecta el STM32 al programador" -ForegroundColor White
Write-Host "3. Ejecuta: python src\programmer.py" -ForegroundColor White
Write-Host "`nO crea un acceso directo al archivo src\programmer.py" -ForegroundColor White

Read-Host "`nPresiona Enter para finalizar"