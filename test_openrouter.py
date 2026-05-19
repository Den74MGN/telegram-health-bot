#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест OpenRouter API
Проверяет подключение и доступные модели
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_openrouter():
    """Тестирует OpenRouter API"""
    
    print("=" * 60)
    print("🧪 ТЕСТ OPENROUTER API")
    print("=" * 60)
    print()
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в .env")
        return False
    
    print(f"✅ API ключ найден: {api_key[:20]}...")
    print()
    
    # Тест 1: Проверка доступных моделей
    print("📋 Тест 1: Получение списка моделей...")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'https://openrouter.ai/api/v1/models',
            headers=headers,
            timeout=10
        )
        
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Подключение успешно!")
            data = response.json()
            models = data.get('data', [])
            
            # Показываем бесплатные модели
            free_models = [m for m in models if 'free' in m.get('id', '').lower()]
            print(f"   📊 Найдено бесплатных моделей: {len(free_models)}")
            
            if free_models:
                print("\n   🆓 Доступные бесплатные модели:")
                for model in free_models[:5]:
                    print(f"      • {model.get('id', 'Unknown')}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False
    
    print()
    
    # Тест 2: Генерация текста
    print("📝 Тест 2: Генерация тестового текста...")
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://telegram-health-bot.com',
            'X-Title': 'Telegram Health Bot'
        }
        
        payload = {
            'model': 'meta-llama/llama-3.3-70b-instruct:free',
            'messages': [
                {
                    'role': 'user',
                    'content': 'Напиши короткий совет о здоровье (1 предложение)'
                }
            ],
            'max_tokens': 100
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            text = data['choices'][0]['message']['content']
            print("   ✅ Генерация успешна!")
            print(f"   📄 Результат: {text[:100]}...")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text[:500]}")
            
            # Дополнительная диагностика
            if response.status_code == 401:
                print("\n   💡 Ошибка 401: Неверный API ключ")
                print("      Проверьте ключ на https://openrouter.ai/keys")
            elif response.status_code == 404:
                print("\n   💡 Ошибка 404: Модель не найдена или недоступна")
                print("      Попробуйте другую модель из списка выше")
            elif response.status_code == 429:
                print("\n   💡 Ошибка 429: Превышен лимит запросов")
                print("      Подождите немного и попробуйте снова")
            
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False
    
    print()
    print("=" * 60)
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)
