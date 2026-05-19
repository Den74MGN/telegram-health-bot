#!/usr/bin/env python3
"""
Простой тест API без эмодзи
"""

import os
import requests
from dotenv import load_dotenv

def main():
    load_dotenv()

    print("Testing Telegram Health Bot APIs")
    print("=" * 40)

    # Test Telegram
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if bot_token:
        try:
            response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data['result']
                    print(f"Telegram OK: @{bot_info['username']}")
                    telegram_ok = True
                else:
                    print(f"Telegram ERROR: {data.get('description')}")
                    telegram_ok = False
            else:
                print(f"Telegram HTTP ERROR: {response.status_code}")
                telegram_ok = False
        except Exception as e:
            print(f"Telegram EXCEPTION: {e}")
            telegram_ok = False
    else:
        print("ERROR: TELEGRAM_BOT_TOKEN not found")
        telegram_ok = False

    # Test OpenRouter
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
                'messages': [{'role': 'user', 'content': 'Hello! Write a short greeting.'}],
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
                print(f"OpenRouter OK: {result[:50]}...")
                openrouter_ok = True
            else:
                print(f"OpenRouter ERROR: {response.status_code}")
                openrouter_ok = False

        except Exception as e:
            print(f"OpenRouter EXCEPTION: {e}")
            openrouter_ok = False
    else:
        print("ERROR: OPENROUTER_API_KEY not found or invalid")
        openrouter_ok = False

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