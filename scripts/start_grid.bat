@echo off
chcp 65001 >nul
setlocal

cd ..

set SELENIUM_JAR=selenium-server-4.41.0.jar

if not exist "%SELENIUM_JAR%" (
    echo Установочный файл Selenium не найден. Начинаем скачивание...
    curl -L -O https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.41.0/%SELENIUM_JAR%
    echo Скачивание завершено!
)

set HUB_PORT=4444
set NODE_PORT=5555

echo Запускаем HUB на порту %HUB_PORT%...
start "Selenium Hub" cmd /k java -jar "%SELENIUM_JAR%" hub --port %HUB_PORT%

echo Ожидание старта HUB...
:WaitHub
:: стучимся в статус хаба, пока он не ответит (код 0)
curl -s http://localhost:%HUB_PORT%/status >nul

if %errorlevel% equ 0 goto HubReady
powershell.exe -Command "Start-Sleep -Seconds 1"

goto WaitHub

:HubReady
echo HUB успешно запущен!


echo Запускаем NODE...
start "Selenium Node" cmd /k java -jar "%SELENIUM_JAR%" node ^
  --port %NODE_PORT% ^
  --hub http://localhost:%HUB_PORT%

echo.
echo Selenium Grid развернут: http://localhost:%HUB_PORT%/ui
pause
endlocal
