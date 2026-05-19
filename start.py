#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Launcher для обхода проблем с docstrings

import sys
import os
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Импортируем модули
from module_content import ContentGenerator
from module_publisher import TelegramPublisher
from module_scheduler import ContentScheduler
from module_analytics import ContentAnalytics
from database_manager import DatabaseManager

print("=" * 60)
print("🚀 ЗАПУСК TELEGRAM HEALTH BOT")
print("=" * 60)
print()

# Инициализация
content_gen = ContentGenerator(os.getenv('OPENROUTER_API_KEY'))
publisher = TelegramPublisher(
    bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
    channel_id=os.getenv('TELEGRAM_CHANNEL_ID'),
    admin_chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID')
)
scheduler = ContentScheduler()
analytics = ContentAnalytics()

# Инициализация базы данных
db_manager = DatabaseManager('data/bot.db')
db_manager.init_database()
print("✅ База данных инициализирована")
print()

# Статистика
stats = {
    'posts_published': 0,
    'start_time': datetime.now()
}

async def generate_and_publish():
    # Генерация и публикация контента
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📝 Генерация контента...")
    
    # Получаем доступные темы из БД (не использовались последние 2 часа для лучшего чередования)
    all_topics = content_gen.topics
    available_topics = db_manager.get_available_topics(all_topics, block_days=0.084)  # 2 часа = 0.084 дня
    
    # Умный выбор темы: приоритет наименее используемым темам
    import random
    if available_topics:
        # Получаем статистику тем
        topic_stats = db_manager.get_topic_statistics()
        topic_usage = {stat['name']: stat['usage_count'] for stat in topic_stats}
        
        # Сортируем доступные темы по количеству использований (меньше = выше приоритет)
        available_with_priority = sorted(
            available_topics, 
            key=lambda t: topic_usage.get(t, 0)
        )
        
        # Выбираем из топ-3 наименее используемых тем для разнообразия
        top_candidates = available_with_priority[:3]
        topic = random.choice(top_candidates)
        
        print(f"   📊 Доступно тем: {len(available_topics)}")
        print(f"   🎯 Выбрана тема с наименьшим использованием: {topic}")
    else:
        # Если все темы заблокированы, выбираем наименее используемую
        topic_stats = db_manager.get_topic_statistics()
        if topic_stats:
            # Сортируем по использованию
            sorted_topics = sorted(topic_stats, key=lambda x: x['usage_count'])
            topic = sorted_topics[0]['name']
            print(f"   ⚠️ Все темы использовались недавно, выбрана наименее используемая: {topic}")
        else:
            # Если статистики нет, выбираем случайную
            topic = random.choice(all_topics)
            print(f"   🎲 Первый запуск, выбрана случайная тема: {topic}")
    
    content = content_gen.generate_text_post(topic)
    
    if not content:
        print("❌ Ошибка генерации")
        return
    
    print(f"✅ Сгенерирован: {content['title']} (тема: {content['topic']})")
    
    # Форматируем caption
    title = f"*{content['title']}*"
    body = content['body']
    hashtags = ' '.join(content.get('hashtags', [])[:5])
    caption = f"{title}\n\n{body}\n\n{hashtags}"
    
    if len(caption) > 1024:
        available = 1024 - len(title) - len(hashtags) - 10
        if available > 100:
            body = body[:available] + "..."
            caption = f"{title}\n\n{body}\n\n{hashtags}"
        else:
            available = 1024 - len(title) - 10
            body = body[:available] + "..."
            caption = f"{title}\n\n{body}"
    
    # Публикуем
    if content.get('image_bytes'):
        success = await publisher.publish_photo_post(content['image_bytes'], caption)
    else:
        success = await publisher.publish_text_post(content)
    
    if success:
        stats['posts_published'] += 1
        print(f"✅ Пост #{stats['posts_published']} опубликован")
        
        # Сохраняем пост в БД
        try:
            post_id = db_manager.save_post(content)
            print(f"💾 Пост сохранен в БД (ID: {post_id})")
        except Exception as e:
            print(f"⚠️ Ошибка сохранения в БД: {e}")
        
        # Записываем аналитику
        analytics.record_post_performance({
            'post_id': f"post_{int(datetime.now().timestamp())}",
            'title': content['title'],
            'topic': content['topic'],
            'body': content['body'],
            'scheduled_date': datetime.now()
        })
    else:
        print("❌ Ошибка публикации")

async def run_scheduled_async():
    # Запуск по расписанию в одном event loop
    interval_hours = int(os.getenv('POST_INTERVAL_HOURS', 6))
    
    print(f"⏰ Интервал публикации: {interval_hours} часов")
    print(f"🕐 Следующая публикация: через {interval_hours} часов")
    print()
    print("Нажмите Ctrl+C для остановки")
    print("=" * 60)
    
    try:
        while True:
            await generate_and_publish()
            
            # Ждем до следующей публикации
            wait_seconds = interval_hours * 3600
            print(f"\n⏳ Ожидание {interval_hours} часов до следующей публикации...")
            await asyncio.sleep(wait_seconds)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен пользователем")
        print(f"📊 Всего опубликовано постов: {stats['posts_published']}")
        print(f"⏱️ Время работы: {datetime.now() - stats['start_time']}")
        
        # Показываем статистику из БД
        total_posts = db_manager.get_total_posts()
        print(f"💾 Всего постов в БД: {total_posts}")
        
        # Создаем резервную копию
        backup_path = db_manager.backup_database()
        if backup_path:
            print(f"💾 Резервная копия БД: {backup_path}")

def run_scheduled():
    # Запуск в одном event loop
    try:
        asyncio.run(run_scheduled_async())
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен")

if __name__ == "__main__":
    run_scheduled()
