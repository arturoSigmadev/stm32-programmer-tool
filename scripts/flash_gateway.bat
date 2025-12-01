@echo off
REM =================================================================
REM  Unified STM32 Gateway Flasher - Windows Batch Wrapper
REM  Provides backward compatibility with old flash_gateway.bat
REM =================================================================

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_ROOT=%~dp0..\..\..\project
set PYTHON=python

REM Print banner
echo.
echo ================================================================
echo   STM32 Gateway Unified Programmer
echo   Build, Flash, and Deploy Tool
echo ================================================================
echo.

REM Check Python
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo [INFO] Please install Python 3.7+ and add to PATH
    pause
    exit /b 1
)

REM Parse arguments
set CLEAN_FLAG=
set NO_BUILD_FLAG=
set CONFIG=Debug

:parse_args
if "%1"=="" goto end_parse
if /i "%1"=="--clean" set CLEAN_FLAG=--clean
if /i "%1"=="--no-build" set NO_BUILD_FLAG=--no-build
if /i "%1"=="--release" set CONFIG=Release
shift
goto parse_args
:end_parse

REM Display configuration
echo [INFO] Project: %PROJECT_ROOT%
echo [INFO] Config: %CONFIG%
if defined CLEAN_FLAG echo [INFO] Clean build enabled
if defined NO_BUILD_FLAG echo [INFO] Build step skipped
echo.

REM Execute deployment
echo [INFO] Starting deployment...
echo.

%PYTHON% -m utils.stm32Programmer.cli.flash_cli deploy "%PROJECT_ROOT%" ^
    --config %CONFIG% ^
    %CLEAN_FLAG% ^
    %NO_BUILD_FLAG%

if errorlevel 1 (
    echo.
    echo ================================================================
    echo   [ERROR] Deployment Failed!
    echo ================================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo   [SUCCESS] Deployment Completed Successfully!
echo ================================================================
echo.

REM Optional: Keep window open
if "%2"=="--pause" pause

exit /b 0
