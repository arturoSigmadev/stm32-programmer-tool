@echo off
REM ========================================
REM Script para crear paquete del cliente
REM ========================================

echo.
echo ========================================
echo EMPAQUETANDO ARCHIVOS PARA CLIENTE
echo ========================================
echo.

REM Definir nombre del paquete
set "PACKAGE_NAME=UQOMM_STM32_Programmer_Package"
set "TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "OUTPUT_DIR=paquete_cliente_%TIMESTAMP%"

echo Creando directorio temporal: %OUTPUT_DIR%
mkdir "%OUTPUT_DIR%" 2>nul

REM Copiar archivos principales
echo.
echo [1/7] Copiando documentacion principal...
copy "LEEME_CLIENTE.md" "%OUTPUT_DIR%\" >nul
copy "GUIA_INSTALACION_CLIENTE.md" "%OUTPUT_DIR%\" >nul
copy "README.md" "%OUTPUT_DIR%\" >nul

REM Copiar herramienta portable
echo [2/7] Copiando herramienta STM32 Programmer...
xcopy "dist\STM32_Programmer_Portable.zip" "%OUTPUT_DIR%\" /I /Y >nul
xcopy "dist\README.md" "%OUTPUT_DIR%\dist\" /I /Y >nul

REM Copiar guia HTML con imagenes
echo [3/7] Copiando guia HTML interactiva...
mkdir "%OUTPUT_DIR%\guia\" 2>nul
copy "uqomm_stm32_programer_guide\stm32_firmware_guide_standalone.html" "%OUTPUT_DIR%\guia\" >nul
xcopy "uqomm_stm32_programer_guide\assets" "%OUTPUT_DIR%\guia\assets\" /E /I /Y >nul

REM Copiar STM32CubeProgrammer
echo [4/7] Copiando STM32CubeProgrammer oficial...
copy "uqomm_stm32_programer_guide\stm32cubeprg-win64-v2-20-0.zip" "%OUTPUT_DIR%\guia\" >nul

REM Copiar documentacion tecnica
echo [5/7] Copiando documentacion tecnica...
xcopy "docs" "%OUTPUT_DIR%\docs\" /E /I /Y >nul

REM Copiar instalador
echo [6/7] Copiando instalador automatico...
copy "INSTALAR.bat" "%OUTPUT_DIR%\" >nul

REM Crear archivo de inicio rapido
echo [7/7] Creando archivo de inicio rapido...
(
echo @echo off
echo REM ========================================
echo REM INICIO RAPIDO - UQOMM STM32 Programmer
echo REM ========================================
echo.
echo echo.
echo echo ========================================
echo echo UQOMM - PROGRAMACION DE FIRMWARE STM32
echo echo ========================================
echo echo.
echo echo Bienvenido al paquete de programacion UQOMM
echo echo.
echo echo POR FAVOR, ELIJA UNA OPCION:
echo echo.
echo echo [1] Abrir Guia HTML Interactiva ^(RECOMENDADO^)
echo echo [2] Ver documentacion en formato texto
echo echo [3] Extraer herramienta portable
echo echo [4] Instalar dependencias ^(Python + OpenOCD^)
echo echo [5] Salir
echo echo.
echo set /p opcion="Ingrese el numero de opcion: "
echo.
echo if "%%opcion%%"=="1" ^(
echo     start guia\stm32_firmware_guide_standalone.html
echo     echo.
echo     echo Guia HTML abierta en el navegador
echo     pause
echo ^)
echo.
echo if "%%opcion%%"=="2" ^(
echo     start LEEME_CLIENTE.md
echo     pause
echo ^)
echo.
echo if "%%opcion%%"=="3" ^(
echo     echo.
echo     echo Extrayendo STM32_Programmer_Portable.zip...
echo     powershell -command "Expand-Archive -Path 'STM32_Programmer_Portable.zip' -DestinationPath '.' -Force"
echo     echo.
echo     echo Herramienta extraida. Puede ejecutar STM32_Programmer.exe
echo     pause
echo ^)
echo.
echo if "%%opcion%%"=="4" ^(
echo     start INSTALAR.bat
echo ^)
echo.
echo if "%%opcion%%"=="5" ^(
echo     exit
echo ^)
echo.
echo goto :eof
) > "%OUTPUT_DIR%\INICIO_RAPIDO.bat"

REM Crear archivo ZIP del paquete completo
echo.
echo ========================================
echo Creando archivo ZIP del paquete...
echo ========================================

powershell -command "Compress-Archive -Path '%OUTPUT_DIR%\*' -DestinationPath '%PACKAGE_NAME%_%TIMESTAMP%.zip' -Force"

if exist "%PACKAGE_NAME%_%TIMESTAMP%.zip" (
    echo.
    echo ========================================
    echo PAQUETE CREADO EXITOSAMENTE
    echo ========================================
    echo.
    echo Archivo: %PACKAGE_NAME%_%TIMESTAMP%.zip
    echo Ubicacion: %CD%
    echo.
    echo El paquete contiene:
    echo   - Guia HTML interactiva con imagenes
    echo   - STM32CubeProgrammer oficial
    echo   - Herramienta portable STM32_Programmer
    echo   - Documentacion completa
    echo   - Instalador automatico
    echo   - Script de inicio rapido
    echo.
    
    REM Preguntar si desea eliminar carpeta temporal
    set /p borrar="Desea eliminar la carpeta temporal? (S/N): "
    if /i "%borrar%"=="S" (
        rmdir /S /Q "%OUTPUT_DIR%"
        echo Carpeta temporal eliminada
    ) else (
        echo Carpeta temporal conservada: %OUTPUT_DIR%
    )
    
    echo.
    echo Presione cualquier tecla para abrir la ubicacion del archivo...
    pause >nul
    explorer /select,"%CD%\%PACKAGE_NAME%_%TIMESTAMP%.zip"
    
) else (
    echo.
    echo ERROR: No se pudo crear el archivo ZIP
    echo Verifique que tiene permisos y espacio suficiente
    pause
)

echo.
echo ========================================
echo PROCESO COMPLETADO
echo ========================================
pause
