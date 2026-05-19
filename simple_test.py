#!/usr/bin/env python3
"""
Простой тест API подключений
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_openrouter():
    """Тест OpenRouter API"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found")
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
            'messages': [{'role': 'user', 'content': 'Hello! Write a short greeting in Russian.'}],
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
            print(f"OpenRouter OK: {result}")
            return True
        else:
            print(f"OpenRouter ERROR: {response.status_code}")
            return False

    except Exception as e:
        print(f"OpenRouter EXCEPTION: {e}")
        return False

def test_telegram():
    """Тест Telegram Bot API"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found")
        return False

    try:
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe', timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"Telegram OK: @{bot_info['username']}")
                return True
            else:
                print(f"Telegram ERROR: {data.get('description')}")
                return False
        else:
            print(f"Telegram HTTP ERROR: {response.status_code}")
            return False

    except Exception as e:
        print(f"Telegram EXCEPTION: {e}")
        return False

def main():
    """Основная функция"""
    print("Testing Telegram Health Bot APIs")
    print("=" * 40)

    telegram_ok = test_telegram()
    openrouter_ok = test_openrouter()

    print("=" * 40)
    print("RESULTS:")
    print(f"Telegram API: {'OK' if telegram_ok else 'ERROR'}")
    print(f"OpenRouter API: {'OK' if openrouter_ok else 'ERROR'}")

    if telegram_ok and openrouter_ok:
        print("SUCCESS: Bot is ready to run!")
        print("Run: python main.py")
    else:
        print("ERROR: Fix API keys and try again")

if __name__ == "__main__":
    main()