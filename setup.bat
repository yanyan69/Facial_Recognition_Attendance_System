@echo off

:: Check if Python 3.8 or higher is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python 3.8 or higher is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/.
    exit /b 1
)

:: Check Python version (must be 3.8 or higher)
for /f "tokens=2 delims= " %%v in ('python --version') do set PYTHON_VERSION=%%v
for /f "delims=." %%a in ("%PYTHON_VERSION%") do set MAJOR_VERSION=%%a
if %MAJOR_VERSION% LSS 3 (
    echo Python version %PYTHON_VERSION% is too old. Please install Python 3.8 or higher.
    exit /b 1
)
for /f "tokens=2 delims=." %%b in ("%PYTHON_VERSION%") do set MINOR_VERSION=%%b
if %MAJOR_VERSION%==3 if %MINOR_VERSION% LSS 8 (
    echo Python version %PYTHON_VERSION% is too old. Please install Python 3.8 or higher.
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    exit /b 1
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found. Please ensure it exists in the project directory.
    exit /b 1
)

:: Install dependencies
echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies. Check requirements.txt or your internet connection.
    exit /b 1
)

:: Provide instructions
echo.
echo Setup complete! The virtual environment is activated.
echo Ensure the YOLO model file 'best.pt' is in the project directory.
echo Ensure a webcam is connected for the live feed.
echo To start the web app, run:
echo     python app.py
echo Then access the web interface at http://127.0.0.1:5000 in a browser.
echo For remote access, consider using ngrok: ngrok http 5000
echo To activate the virtual environment in new sessions, run:
echo     venv\Scripts\activate
echo.
pause