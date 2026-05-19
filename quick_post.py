#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для быстрой тестовой публикации
Создает и публикует один пост немедленно
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Импортируем модули бота
from module_content import ContentGenerator
from module_publisher import TelegramPublisher

async def quick_post():
    """Создает и публикует один тестовый пост"""
    
    print("=" * 60)
    print("🚀 БЫСТРАЯ ТЕСТОВАЯ ПУБЛИКАЦИЯ")
    print("=" * 60)
    print()
    
    # Проверяем переменные окружения
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHANNEL_ID',
        'TELEGRAM_ADMIN_CHAT_ID',
        'OPENROUTER_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("❌ Ошибка: Не настроены переменные окружения:")
        for var in missing:
            print(f"   - {var}")
        print()
        print("📝 Создайте файл .env и заполните параметры")
        return False
    
    print("✅ Переменные окружения настроены")
    print()
    
    try:
        # Инициализируем модули
        print("🔧 Инициализация модулей...")
        content_gen = ContentGenerator(os.getenv('OPENROUTER_API_KEY'))
        publisher = TelegramPublisher(
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            channel_id=os.getenv('TELEGRAM_CHANNEL_ID'),
            admin_chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        )
        print("✅ Модули инициализированы")
        print()
        
        # Тестируем подключение к Telegram
        print("🔌 Проверка подключения к Telegram...")
        if not await publisher.test_connection():
            print("❌ Не удалось подключиться к Telegram")
            print("   Проверьте токен бота и интернет соединение")
            return False
        print("✅ Подключение к Telegram успешно")
        print()
        
        # Генерируем контент
        print("📝 Генерация контента...")
        print("   (это может занять 10-30 секунд)")
        content = content_gen.generate_text_post()
        
        if not content:
            print("❌ Не удалось сгенерировать контент")
            return False
        
        print("✅ Контент сгенерирован:")
        print(f"   Заголовок: {content['title']}")
        print(f"   Длина: {len(content['body'])} символов")
        print(f"   Тема: {content['topic']}")
        if content.get('image_bytes'):
            print(f"   Изображение: {len(content['image_bytes'])} байт")
        print()
        
        # Публикуем пост
        print("📤 Публикация поста...")
        
        if content.get('image_bytes'):
            # Форматируем caption с учетом ограничений Telegram
            title = f"*{content['title']}*"
            body = content['body']
            hashtags = ' '.join(content.get('hashtags', [])[:5])
            
            caption = f"{title}\n\n{body}\n\n{hashtags}"
            
            # Проверяем длину и обрезаем если нужно
            if len(caption) > 1024:
                available_for_body = 1024 - len(title) - len(hashtags) - 10
                if available_for_body > 100:
                    body = body[:available_for_body] + "..."
                    caption = f"{title}\n\n{body}\n\n{hashtags}"
                else:
                    available_for_body = 1024 - len(title) - 10
                    body = body[:available_for_body] + "..."
                    caption = f"{title}\n\n{body}"
            
            # Публикуем с изображением
            success = await publisher.publish_photo_post(
                content['image_bytes'],
                caption
            )
        else:
            # Публикуем текстовый пост
            success = await publisher.publish_text_post(content)
        
        if success:
            print("✅ Пост успешно опубликован!")
            print()
            print("🎉 ГОТОВО!")
            print(f"📱 Проверьте ваш канал: {os.getenv('TELEGRAM_CHANNEL_ID')}")
            return True
        else:
            print("❌ Не удалось опубликовать пост")
            print("   Проверьте:")
            print("   - Бот добавлен в канал как администратор")
            print("   - ID канала правильный")
            print("   - У бота есть права на публикацию")
            return False
    
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
        return False
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        logger.exception("Детали ошибки:")
        return False

def main():
    """Главная функция"""
    try:
        result = asyncio.run(quick_post())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
