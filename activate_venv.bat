@echo off
echo 🐍 Activating Lepida Voice Assistant Virtual Environment...
echo.

if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Please run: python setup_assistant.py
    pause
    exit /b 1
)

echo ✅ Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 🎉 Virtual environment activated!
echo You can now run:
echo   - python app.py          (Start voice assistant)
echo   - python cli.py health   (Check system health)
echo   - python cli.py run      (Run voice assistant with CLI)
echo   - cd frontend && python app.py  (Start web interface)
echo.
echo To deactivate, type: deactivate
echo.

cmd /k
