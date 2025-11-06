#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un ejecutable standalone del STM32 Programmer Tool
Requiere PyInstaller instalado: pip install pyinstaller
"""

import os
import sys
import subprocess
import shutil

def create_executable():
    """Crear ejecutable standalone usando PyInstaller"""

    print("🔨 Creando ejecutable del STM32 Programmer Tool...")

    # Verificar que estamos en el directorio correcto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    src_dir = os.path.join(project_root, 'src')
    main_script = os.path.join(src_dir, 'programmer.py')

    if not os.path.exists(main_script):
        print(f"❌ No se encuentra el script principal: {main_script}")
        return False

    # Verificar PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller instalado")

    # Crear directorio de distribución
    dist_dir = os.path.join(project_root, 'dist')
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Un solo archivo ejecutable
        '--windowed',                   # No mostrar consola (ventana)
        '--name=STM32_Programmer',      # Nombre del ejecutable
        '--distpath=dist',              # Directorio de salida
        '--workpath=build',             # Directorio temporal
        '--clean',                      # Limpiar archivos temporales
        '--noconfirm',                  # No pedir confirmación
        # Incluir icono si existe
        # '--icon=icon.ico',
        main_script
    ]

    try:
        result = subprocess.run(cmd, cwd=project_root, check=True, capture_output=True, text=True)
        print("✅ Ejecutable creado exitosamente")
        print(f"📁 Ubicación: {os.path.join(dist_dir, 'STM32_Programmer.exe')}")

        # Verificar que el ejecutable existe
        exe_path = os.path.join(dist_dir, 'STM32_Programmer.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"📏 Tamaño del ejecutable: {file_size:.2f} MB")
        else:
            print("❌ El ejecutable no se creó correctamente")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear el ejecutable: {e}")
        print(f"Salida de error: {e.stderr}")
        return False

    # Crear archivo README para distribución
    create_distribution_readme(project_root, dist_dir)

    return True

def create_distribution_readme(project_root, dist_dir):
    """Crear README para la distribución"""

    readme_content = """# STM32 Programmer Tool - Versión Distribuible

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
"""

    readme_path = os.path.join(dist_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README de distribución creado: {readme_path}")

def create_portable_package(project_root, dist_dir):
    """Crear paquete portable con todos los archivos necesarios"""

    print("📦 Creando paquete portable...")

    portable_dir = os.path.join(dist_dir, 'STM32_Programmer_Portable')

    # Crear estructura
    os.makedirs(portable_dir, exist_ok=True)
    os.makedirs(os.path.join(portable_dir, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(portable_dir, 'docs'), exist_ok=True)

    # Copiar ejecutable
    exe_src = os.path.join(dist_dir, 'STM32_Programmer.exe')
    exe_dst = os.path.join(portable_dir, 'STM32_Programmer.exe')
    if os.path.exists(exe_src):
        shutil.copy2(exe_src, exe_dst)

    # Copiar scripts de instalación
    scripts_src = os.path.join(project_root, 'scripts')
    scripts_dst = os.path.join(portable_dir, 'scripts')
    if os.path.exists(scripts_src):
        for file in os.listdir(scripts_src):
            if file.endswith(('.bat', '.ps1', '.sh')):
                shutil.copy2(os.path.join(scripts_src, file), scripts_dst)

    # Copiar documentación
    docs_src = os.path.join(project_root, 'docs')
    docs_dst = os.path.join(portable_dir, 'docs')
    if os.path.exists(docs_src):
        for file in os.listdir(docs_src):
            if file.endswith('.md'):
                shutil.copy2(os.path.join(docs_src, file), docs_dst)

    # Copiar README de distribución
    readme_src = os.path.join(dist_dir, 'README.md')
    readme_dst = os.path.join(portable_dir, 'README.md')
    if os.path.exists(readme_src):
        shutil.copy2(readme_src, readme_dst)

    # Crear script de inicio rápido
    quick_start = os.path.join(portable_dir, 'INICIAR.bat')
    with open(quick_start, 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo Iniciando STM32 Programmer Tool...\n')
        f.write('STM32_Programmer.exe\n')
        f.write('pause\n')

    print(f"✅ Paquete portable creado: {portable_dir}")

    # Crear archivo ZIP
    zip_name = 'STM32_Programmer_Portable'
    zip_path = os.path.join(dist_dir, zip_name)

    try:
        shutil.make_archive(zip_path, 'zip', portable_dir)
        print(f"✅ Archivo ZIP creado: {zip_path}.zip")
    except Exception as e:
        print(f"⚠️ No se pudo crear ZIP: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando creación de ejecutable...")

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if create_executable():
        dist_dir = os.path.join(project_root, 'dist')
        create_portable_package(project_root, dist_dir)

        print("\n" + "="*50)
        print("✅ DISTRIBUCIÓN COMPLETADA")
        print("="*50)
        print("Archivos generados en la carpeta 'dist':")
        print("- STM32_Programmer.exe (ejecutable)")
        print("- README.md (instrucciones)")
        print("- STM32_Programmer_Portable/ (paquete completo)")
        print("- STM32_Programmer_Portable.zip (opcional)")
        print("\nPara distribuir:")
        print("1. Copia la carpeta 'dist' completa")
        print("2. O comparte el archivo ZIP")
        print("3. Los usuarios solo necesitan ejecutar el .exe")
    else:
        print("❌ Error al crear la distribución")
        sys.exit(1)