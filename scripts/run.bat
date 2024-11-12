@echo off
setlocal

:: Function to cleanup processes
:cleanup
echo.
echo Shutting down services...
taskkill /F /PID %SERVER_PID% 2>nul
taskkill /F /PID %CLIENT_PID% 2>nul
exit /b

:: Get the project root directory
set "PROJECT_ROOT=%~dp0.."

:: Activate virtual environment if it exists
if exist "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
    call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
)

:: Create necessary directories
mkdir "%PROJECT_ROOT%\backend\app\api" 2>nul
mkdir "%PROJECT_ROOT%\backend\app\core" 2>nul
mkdir "%PROJECT_ROOT%\backend\app\models" 2>nul
mkdir "%PROJECT_ROOT%\backend\config" 2>nul
mkdir "%PROJECT_ROOT%\frontend\app\utils" 2>nul
mkdir "%PROJECT_ROOT%\frontend\config" 2>nul

:: Add project root to PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%"

:: Start FastAPI server
echo Starting FastAPI server...
cd "%PROJECT_ROOT%\backend" && start /b cmd /c "python main.py" > nul
for /f "tokens=2" %%a in ('tasklist ^| findstr "python.exe"') do set SERVER_PID=%%a

:: Wait for server to start
timeout /t 2 /nobreak > nul

:: Start Streamlit client
echo Starting Streamlit client...
cd "%PROJECT_ROOT%\frontend" && start /b cmd /c "streamlit run app/main.py" > nul
for /f "tokens=2" %%a in ('tasklist ^| findstr "streamlit"') do set CLIENT_PID=%%a

:: Wait for user to press Ctrl+C
echo Press Ctrl+C to stop the services...
:loop
timeout /t 1 /nobreak > nul
goto loop 