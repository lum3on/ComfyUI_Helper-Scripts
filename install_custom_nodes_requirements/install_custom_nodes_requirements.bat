@echo off
setlocal EnableDelayedExpansion

:: Get the directory where the batch script is located (C:\Tools\Comfy-Portable)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Assume ComfyUI is in a subdirectory named 'ComfyUI'
set "COMFYUI_DIR=%SCRIPT_DIR%\ComfyUI"
set "VENV_PATH=%COMFYUI_DIR%\venv"
set "SCRIPT_PATH=%COMFYUI_DIR%\install_custom_nodes_requirements.py"

:: Check if ComfyUI directory exists
if not exist "%COMFYUI_DIR%" (
    echo Error: ComfyUI directory not found at %COMFYUI_DIR%
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Error: Virtual environment not found at %VENV_PATH%
    pause
    exit /b 1
)

:: Check if install_custom_nodes_requirements.py exists
if not exist "%SCRIPT_PATH%" (
    echo Error: install_custom_nodes_requirements.py not found at %SCRIPT_PATH%
    pause
    exit /b 1
)

echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate virtual environment at %VENV_PATH%
    pause
    exit /b %ERRORLEVEL%
)

echo Running install_custom_nodes_requirements.py...
cd /d "%COMFYUI_DIR%"
python "%SCRIPT_PATH%"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to execute install_custom_nodes_requirements.py
    pause
    exit /b %ERRORLEVEL%
)

echo Installation complete.
pause
endlocal