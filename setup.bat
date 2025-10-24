```bat
@echo off

:: Check if Python 3 is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
echo Python 3 is not installed. Please install Python 3.8 or higher.
exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Check if requirements.txt exists
if not exist requirements.txt (
echo requirements.txt not found. Please ensure it exists in the project directory.
exit /b 1
)

:: Install dependencies
echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete! Virtual environment is activated.
echo Run 'venv\Scripts\activate' to activate the virtual environment in new sessions.
echo Run 'python app.py' to start the Flask server.
pause
```