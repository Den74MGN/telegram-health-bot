#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки и исправления .env файла
Помогает найти и исправить проблемы с конфигурацией
"""

import os
import sys

def check_env_file():
    """Проверяет .env файл на наличие проблем"""
    
    print("=" * 60)
    print("🔍 ПРОВЕРКА .ENV ФАЙЛА")
    print("=" * 60)
    print()
    
    # Проверка существования файла
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print()
        print("📝 Создайте файл .env:")
        print("   1. Скопируйте .env.example в .env")
        print("   2. Заполните обязательные параметры")
        print()
        print("Команда: copy .env.example .env")
        return False
    
    print("✅ Файл .env найден")
    print()
    
    # Читаем файл
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Проверяем обязательные параметры
    required_params = {
        'TELEGRAM_BOT_TOKEN': 'Токен от @BotFather',
        'TELEGRAM_CHANNEL_ID': 'ID канала (например: @my_channel)',
        'TELEGRAM_ADMIN_CHAT_ID': 'Ваш Telegram ID',
        'OPENROUTER_API_KEY': 'API ключ OpenRouter'
    }
    
    found_params = {}
    issues = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if key in required_params:
                found_params[key] = value
    
    # Проверяем каждый параметр
    print("📋 Проверка обязательных параметров:")
    print()
    
    all_ok = True
    
    for param, description in required_params.items():
        value = found_params.get(param, '')
        
        if not value:
            print(f"❌ {param}")
            print(f"   Описание: {description}")
            print(f"   Проблема: Не заполнен")
            issues.append(f"{param} не заполнен")
            all_ok = False
        elif 'your_' in value.lower() or value == 'your_bot_token_here':
            print(f"⚠️  {param}")
            print(f"   Описание: {description}")
            print(f"   Проблема: Содержит placeholder значение")
            print(f"   Текущее значение: {value}")
            issues.append(f"{param} содержит placeholder")
            all_ok = False
        else:
            # Дополнительные проверки
            if param == 'TELEGRAM_BOT_TOKEN':
                if ':' not in value:
                    print(f"⚠️  {param}")
                    print(f"   Проблема: Неверный формат токена")
                    print(f"   Ожидается: 1234567890:ABCdef...")
                    issues.append(f"{param} неверный формат")
                    all_ok = False
                else:
                    print(f"✅ {param}")
                    print(f"   Значение: {value[:20]}...")
            
            elif param == 'TELEGRAM_CHANNEL_ID':
                if not (value.startswith('@') or value.startswith('-100')):
                    print(f"⚠️  {param}")
                    print(f"   Проблема: Неверный формат ID канала")
                    print(f"   Ожидается: @channel или -1001234567890")
                    issues.append(f"{param} неверный формат")
                    all_ok = False
                else:
                    print(f"✅ {param}")
                    print(f"   Значение: {value}")
            
            elif param == 'OPENROUTER_API_KEY':
                if not value.startswith('sk-or-v1-'):
                    print(f"⚠️  {param}")
                    print(f"   Проблема: Неверный формат ключа")
                    print(f"   Ожидается: sk-or-v1-...")
                    print(f"   Текущее: {value[:20]}...")
                    issues.append(f"{param} неверный формат")
                    all_ok = False
                else:
                    print(f"✅ {param}")
                    print(f"   Значение: {value[:30]}...")
            
            else:
                print(f"✅ {param}")
                print(f"   Значение: {value[:30]}...")
        
        print()
    
    # Итоги
    print("=" * 60)
    if all_ok:
        print("🎉 ВСЕ ПАРАМЕТРЫ НАСТРОЕНЫ ПРАВИЛЬНО!")
        print()
        print("Следующий шаг: python test_setup.py")
    else:
        print("❌ НАЙДЕНЫ ПРОБЛЕМЫ:")
        print()
        for issue in issues:
            print(f"   • {issue}")
        print()
        print("📝 Исправьте проблемы в файле .env и запустите снова")
        print()
        print("💡 Инструкции:")
        print("   • TELEGRAM_BOT_TOKEN: Получите от @BotFather")
        print("   • TELEGRAM_CHANNEL_ID: Формат @channel или -1001234567890")
        print("   • TELEGRAM_ADMIN_CHAT_ID: Узнайте у @userinfobot")
        print("   • OPENROUTER_API_KEY: Создайте на https://openrouter.ai/keys")
    
    print("=" * 60)
    
    return all_ok

if __name__ == "__main__":
    success = check_env_file()
    sys.exit(0 if success else 1)
