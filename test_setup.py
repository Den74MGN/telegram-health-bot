#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования настройки бота
Проверяет все необходимые компоненты перед запуском
"""

import os
import sys
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv()

def print_status(message, status):
    """Печатает статус с цветом"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def test_env_variables():
    """Проверяет наличие обязательных переменных окружения"""
    print("\n🔍 Проверка переменных окружения...")
    
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Токен Telegram бота',
        'TELEGRAM_CHANNEL_ID': 'ID канала Telegram',
        'TELEGRAM_ADMIN_CHAT_ID': 'ID администратора',
        'OPENROUTER_API_KEY': 'API ключ OpenRouter'
    }
    
    all_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here' and 'your_' not in value:
            print_status(f"{description}: Настроено", True)
        else:
            print_status(f"{description}: НЕ НАСТРОЕНО", False)
            all_ok = False
    
    return all_ok

def test_telegram_token():
    """Проверяет валидность Telegram токена"""
    print("\n🤖 Проверка Telegram токена...")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token or 'your_' in token:
        return print_status("Токен не настроен", False)
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_name = data['result'].get('username', 'Unknown')
                return print_status(f"Токен валиден (@{bot_name})", True)
        
        return print_status("Токен невалиден", False)
    
    except Exception as e:
        return print_status(f"Ошибка проверки токена: {e}", False)

def test_openrouter_api():
    """Проверяет OpenRouter API ключ"""
    print("\n🧠 Проверка OpenRouter API...")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key or 'your_' in api_key:
        return print_status("API ключ не настроен", False)
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Простой запрос для проверки ключа
        response = requests.get(
            'https://openrouter.ai/api/v1/models',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return print_status("OpenRouter API ключ валиден", True)
        elif response.status_code == 401:
            print_status("OpenRouter API ошибка: 401 (Неверный ключ)", False)
            print("   💡 Проверьте ключ на https://openrouter.ai/keys")
            return False
        elif response.status_code == 404:
            print_status("OpenRouter API ошибка: 404", False)
            print("   💡 Возможно, ключ устарел или неактивен")
            print("   💡 Создайте новый ключ на https://openrouter.ai/keys")
            return False
        else:
            print_status(f"OpenRouter API ошибка: {response.status_code}", False)
            print(f"   Ответ: {response.text[:200]}")
            return False
    
    except Exception as e:
        return print_status(f"Ошибка проверки OpenRouter: {e}", False)

def test_pollinations():
    """Проверяет доступность Pollinations.ai"""
    print("\n🎨 Проверка Pollinations.ai...")
    
    try:
        response = requests.head(
            'https://image.pollinations.ai/prompt/test',
            timeout=10
        )
        
        if response.status_code in [200, 302]:
            return print_status("Pollinations.ai доступен (бесплатно!)", True)
        else:
            return print_status("Pollinations.ai недоступен", False)
    
    except Exception as e:
        return print_status(f"Ошибка проверки Pollinations: {e}", False)

def test_dependencies():
    """Проверяет установленные зависимости"""
    print("\n📦 Проверка зависимостей...")
    
    required_packages = [
        'telegram',
        'apscheduler',
        'requests',
        'dotenv',
        'PIL',
        'pandas'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"Пакет {package}: Установлен", True)
        except ImportError:
            print_status(f"Пакет {package}: НЕ УСТАНОВЛЕН", False)
            all_ok = False
    
    return all_ok

def test_directories():
    """Проверяет наличие необходимых директорий"""
    print("\n📁 Проверка директорий...")
    
    directories = ['logs', 'data', 'cache', 'backups']
    
    for directory in directories:
        if os.path.exists(directory):
            print_status(f"Директория {directory}: Существует", True)
        else:
            os.makedirs(directory, exist_ok=True)
            print_status(f"Директория {directory}: Создана", True)
    
    return True

def main():
    """Главная функция тестирования"""
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ НАСТРОЙКИ TELEGRAM HEALTH BOT")
    print("=" * 60)
    
    # Проверяем .env файл
    if not os.path.exists('.env'):
        print("\n❌ Файл .env не найден!")
        print("📝 Скопируйте .env.example в .env и заполните параметры")
        print("\nКоманда: copy .env.example .env")
        sys.exit(1)
    
    # Запускаем тесты
    results = []
    
    results.append(("Переменные окружения", test_env_variables()))
    results.append(("Telegram токен", test_telegram_token()))
    results.append(("OpenRouter API", test_openrouter_api()))
    results.append(("Pollinations.ai", test_pollinations()))
    results.append(("Зависимости", test_dependencies()))
    results.append(("Директории", test_directories()))
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    for test_name, status in results:
        print_status(test_name, status)
    
    print(f"\n✅ Пройдено: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 Бот готов к запуску: python main.py")
        return 0
    else:
        print(f"\n⚠️ Не пройдено тестов: {total - passed}")
        print("📝 Исправьте ошибки перед запуском бота")
        return 1

if __name__ == "__main__":
    sys.exit(main())
