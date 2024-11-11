@echo off
setlocal

:: Function to cleanup processes
:cleanup
echo.
echo Shutting down services...
taskkill /F /PID %SERVER_PID% 2>nul
taskkill /F /PID %CLIENT_PID% 2>nul
exit /b

:: Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

:: Start FastAPI server
echo Starting FastAPI server...
cd backend && start /b cmd /c "python main.py" > nul
for /f "tokens=2" %%a in ('tasklist ^| findstr "python.exe"') do set SERVER_PID=%%a

:: Wait for server to start
timeout /t 2 /nobreak > nul

:: Start Streamlit client
echo Starting Streamlit client...
cd ../frontend && start /b cmd /c "streamlit run app/pages/home.py" > nul
for /f "tokens=2" %%a in ('tasklist ^| findstr "streamlit"') do set CLIENT_PID=%%a

:: Wait for user to press Ctrl+C
echo Press Ctrl+C to stop the services...
:loop
timeout /t 1 /nobreak > nul
goto loop 