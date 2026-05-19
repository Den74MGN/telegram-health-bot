#!/usr/bin/env python3
"""
Тест и запуск бота - работает из любой директории
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

def find_project_root():
    """Находит корневую директорию проекта"""
    current_path = Path(__file__).resolve()

    # Ищем .env файл в текущей или родительских директориях
    for path in [current_path] + list(current_path.parents):
        env_file = path / '.env'
        if env_file.exists():
            return path

    # Если не нашли, предполагаем что скрипт в корне проекта
    return current_path.parent

def test_apis():
    """Тестируем API подключения"""
    project_root = find_project_root()
    os.chdir(project_root)

    # Загружаем переменные окружения
    load_dotenv()

    print("🧪 Тестирование API подключений...")
    print("=" * 50)

    # Тест Telegram
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if bot_token:
        try:
            response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data['result']
                    print(f"✅ Telegram бот активен: @{bot_info['username']}")
                    telegram_ok = True
                else:
                    print(f"❌ Ошибка Telegram API: {data.get('description')}")
                    telegram_ok = False
            else:
                print(f"❌ HTTP ошибка Telegram: {response.status_code}")
                telegram_ok = False
        except Exception as e:
            print(f"❌ Ошибка подключения к Telegram: {e}")
            telegram_ok = False
    else:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env")
        telegram_ok = False

    # Тест OpenRouter
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key and api_key.startswith('sk-or-v1-'):
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://telegram-health-bot.com',
                'X-Title': 'Telegram Health Bot'
            }

            payload = {
                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                'messages': [{'role': 'user', 'content': 'Привет! Напиши короткое приветствие.'}],
                'max_tokens': 50,
                'temperature': 0.7
            }

            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                result = data['choices'][0]['message']['content'].strip()
                print(f"✅ OpenRouter работает: {result[:50]}...")
                openrouter_ok = True
            else:
                print(f"❌ OpenRouter ошибка: {response.status_code}")
                openrouter_ok = False

        except Exception as e:
            print(f"❌ Ошибка OpenRouter: {e}")
            openrouter_ok = False
    else:
        print("❌ OPENROUTER_API_KEY не найден или некорректный")
        openrouter_ok = False

    return telegram_ok and openrouter_ok

def create_directories():
    """Создаем необходимые директории"""
    project_root = find_project_root()
    os.chdir(project_root)

    dirs = ['logs', 'content', 'analytics', 'analytics/charts', 'backups']
    for dir_name in dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ Создана директория: {dir_name}")
        except Exception as e:
            print(f"❌ Ошибка создания {dir_name}: {e}")

def run_bot():
    """Запускаем бота"""
    project_root = find_project_root()
    os.chdir(project_root)

    print("🚀 Запуск Telegram бота здоровья...")

    try:
        # Создаем директории
        create_directories()

        # Проверяем API
        if test_apis():
            print("✅ Все API работают - запускаем бота...")
            result = os.system(f"{sys.executable} main.py")
            return result == 0
        else:
            print("❌ Проблемы с API - проверьте настройки")
            return False

    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False

def main():
    """Главная функция"""
    print("🤖 Telegram Бот Здоровья - Автоматический Запуск")
    print("=" * 60)

    # Находим проект
    project_root = find_project_root()
    print(f"📁 Проект найден: {project_root}")

    # Проверяем .env файл
    env_file = project_root / '.env'
    if env_file.exists():
        print("✅ Файл конфигурации найден")
    else:
        print("❌ Файл .env не найден!")
        print("💡 Создайте .env файл с вашими API ключами")
        return

    # Тестируем и запускаем
    if run_bot():
        print("🎉 Бот успешно запущен!")
        print("📱 Проверьте ваш канал - посты будут появляться каждые 2 часа")
    else:
        print("❌ Не удалось запустить бота")
        print("💡 Проверьте настройки в .env файле")

if __name__ == "__main__":
    main()