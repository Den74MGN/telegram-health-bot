@echo off
chcp 65001 >nul
title Telegram Health Bot

echo ========================================
echo 🤖 TELEGRAM HEALTH BOT
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo 📥 Скачайте Python с https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python установлен
echo.

REM Проверка .env файла
if not exist .env (
    echo ❌ Файл .env не найден!
    echo.
    echo 📝 Создайте файл .env из .env.example:
    echo    1. Скопируйте .env.example в .env
    echo    2. Заполните обязательные параметры
    echo.
    if exist .env.example (
        echo 💡 Хотите создать .env сейчас? (Y/N)
        set /p create_env=
        if /i "%create_env%"=="Y" (
            copy .env.example .env
            echo ✅ Файл .env создан
            echo 📝 Откройте .env и заполните параметры
            notepad .env
            pause
            exit /b 0
        )
    )
    pause
    exit /b 1
)

echo ✅ Файл .env найден
echo.

REM Проверка зависимостей
echo 📦 Проверка зависимостей...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Зависимости не установлены
    echo 📥 Устанавливаю зависимости...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости установлены
)
echo.

REM Тестирование настройки
echo 🧪 Запуск тестов...
python test_setup.py
if errorlevel 1 (
    echo.
    echo ⚠️ Тесты не пройдены
    echo 📝 Исправьте ошибки и запустите снова
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🚀 ЗАПУСК БОТА
echo ========================================
echo.
echo Бот будет работать в фоновом режиме
echo Для остановки нажмите Ctrl+C
echo.
echo Логи сохраняются в папке logs/
echo.

REM Запуск бота
python main.py

REM Если бот завершился с ошибкой
if errorlevel 1 (
    echo.
    echo ❌ Бот завершился с ошибкой
    echo 📝 Проверьте логи в папке logs/
    pause
    exit /b 1
)

pause
