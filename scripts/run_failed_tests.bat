@echo off
chcp 65001 >nul
setlocal

cd ..

echo Активация виртуального окружения...
call .venv\Scripts\activate

echo Запуск только упавших тестов с предыдущего прогона...
pytest tests/ --lf -v -n auto

echo.
pause
endlocal
