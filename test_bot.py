#!/usr/bin/env python3
"""
Простой тест бота для проверки работы с вашими ключами
"""

import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_openrouter():
    """Тест OpenRouter API"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в .env файле")
        return False

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://telegram-health-bot.com',
            'X-Title': 'Telegram Health Bot'
        }

        payload = {
            'model': 'meta-llama/llama-3.1-8b-instruct:free',
            'messages': [{'role': 'user', 'content': 'Привет! Напиши короткое приветствие на русском.'}],
            'max_tokens': 100,
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
            print(f"✅ OpenRouter работает! Ответ: {result}")
            return True
        else:
            print(f"❌ OpenRouter API ошибка: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Ошибка подключения к OpenRouter: {e}")
        return False

def test_telegram():
    """Тест Telegram Bot API"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env файле")
        return False

    try:
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe', timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Telegram бот активен: @{bot_info['username']}")
                return True
            else:
                print(f"❌ Ошибка Telegram API: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP ошибка Telegram: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование Telegram бота здоровья")
    print("=" * 50)

    # Тест Telegram
    print("\n📱 Тест Telegram Bot API:")
    telegram_ok = test_telegram()

    # Тест OpenRouter
    print("\n🤖 Тест OpenRouter API:")
    openrouter_ok = test_openrouter()

    # Результаты
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"• Telegram API: {'✅ Работает' if telegram_ok else '❌ Проблемы'}")
    print(f"• OpenRouter API: {'✅ Работает' if openrouter_ok else '❌ Проблемы'}")

    if telegram_ok and openrouter_ok:
        print("\n🎉 Все тесты пройдены! Бот готов к запуску.")
        print("💡 Для запуска выполните: python main.py")
    else:
        print("\n⚠️ Есть проблемы с подключением.")
        print("📖 Проверьте инструкции в файлах:")
        print("   - get_ids_tokens.md")
        print("   - openrouter_setup.md")
        print("   - START_HERE.md")

if __name__ == "__main__":
    main()