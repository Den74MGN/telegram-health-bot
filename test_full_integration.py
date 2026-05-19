#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полный интеграционный тест всех модулей.
Проверяет работу всей системы вместе.
"""

import os
from prompts import create_image_prompt, get_available_topics
from optimizer import format_caption, validate_length, get_text_stats
from database import Database
from deduplicator import Deduplicator
from analytics import Analytics
from notifications import NotificationManager


def test_complete_workflow():
    """
    Тестирует полный рабочий процесс всех модулей:
    1. Инициализация всех компонентов
    2. Выбор темы через дедупликатор
    3. Генерация промпта для изображения
    4. Оптимизация текста
    5. Сохранение в БД
    6. Аналитика
    7. Уведомления
    """
    print("=" * 70)
    print("ПОЛНЫЙ ИНТЕГРАЦИОННЫЙ ТЕСТ ВСЕХ МОДУЛЕЙ")
    print("=" * 70)
    
    # Подготовка
    test_db_path = 'data/test_full_integration.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Удаляем лог уведомлений
    log_file = 'logs/notifications.log'
    if os.path.exists(log_file):
        os.remove(log_file)
    
    try:
        # ШАГ 1: Инициализация всех компонентов
        print("\n🔧 ШАГ 1: Инициализация компонентов")
        print("-" * 70)
        
        # База данных
        db = Database(test_db_path)
        db.connect()
        db.init_tables()
        print("   ✅ База данных инициализирована")
        
        # Дедупликатор
        dedup = Deduplicator(db, block_days=7)
        print("   ✅ Дедупликатор создан")
        
        # Аналитика
        analytics = Analytics(db)
        print("   ✅ Аналитика создана")
        
        # Уведомления
        notifier = NotificationManager(admin_chat_id='123456789')
        print("   ✅ Менеджер уведомлений создан")
        
        # Отправляем уведомление о запуске
        notifier.send_startup_notification()
        print("   ✅ Уведомление о запуске отправлено")
        
        # ШАГ 2: Симуляция работы бота (несколько циклов)
        print("\n🔄 ШАГ 2: Симуляция работы бота")
        print("-" * 70)
        
        topics = get_available_topics()[:8]  # Берем 8 тем
        print(f"   Доступно тем: {len(topics)}")
        
        # Создаем 10 постов
        for i in range(10):
            print(f"\n   📝 Пост #{i+1}:")
            
            # 2.1: Выбор темы
            topic = dedup.get_best_topic(topics)
            print(f"      Тема: {topic}")
            
            # 2.2: Генерация промпта
            title = f"Полезный совет #{i+1} по теме {topic}"
            image_prompt = create_image_prompt(topic, title)
            print(f"      Промпт: {len(image_prompt)} символов")
            
            # 2.3: Создание контента
            body = f"Это полезный совет номер {i+1} по теме '{topic}'. " * 5
            hashtags = [f'#{topic.replace(" ", "")}', '#здоровье', '#совет', f'#пост{i+1}']
            
            # 2.4: Оптимизация текста
            caption = format_caption(title, body, hashtags)
            stats = get_text_stats(caption)
            print(f"      Caption: {stats['length']} символов, валидно: {stats['valid']}")
            
            # 2.5: Сохранение в БД
            try:
                post_id = db.save_post(title, body, topic)
                print(f"      ✅ Сохранен в БД (ID: {post_id})")
                
                # 2.6: Уведомление об успехе
                notifier.send_success_notification(title, topic)
                
            except Exception as e:
                print(f"      ❌ Ошибка сохранения: {e}")
                notifier.send_error_notification(str(e), f"Пост #{i+1}")
        
        # ШАГ 3: Анализ результатов
        print("\n📊 ШАГ 3: Анализ результатов")
        print("-" * 70)
        
        # 3.1: Общая статистика
        total_posts = analytics.get_total_posts()
        print(f"   Всего постов создано: {total_posts}")
        
        # 3.2: Распределение по темам
        distribution = analytics.get_topic_distribution()
        print(f"   Уникальных тем использовано: {len(distribution)}")
        
        print("   Распределение по темам:")
        for topic, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_posts * 100) if total_posts > 0 else 0
            print(f"      • {topic}: {count} ({percentage:.1f}%)")
        
        # 3.3: Топ темы
        top_topics = analytics.get_top_topics(limit=5)
        print(f"\n   Топ-5 тем:")
        for i, topic_stat in enumerate(top_topics, 1):
            print(f"      {i}. {topic_stat['name']}: {topic_stat['usage_count']} постов")
        
        # 3.4: Частота публикаций
        frequency = analytics.get_posting_frequency(days=1)
        print(f"\n   Частота публикаций: {frequency} постов/день")
        
        # ШАГ 4: Проверка дедупликации
        print("\n🔄 ШАГ 4: Проверка дедупликации")
        print("-" * 70)
        
        # 4.1: Проверяем заблокированные темы
        blocked_topics = []
        available_topics = []
        
        for topic in topics:
            if dedup.is_available(topic):
                available_topics.append(topic)
            else:
                blocked_topics.append(topic)
        
        print(f"   Заблокированных тем: {len(blocked_topics)}")
        print(f"   Доступных тем: {len(available_topics)}")
        
        if blocked_topics:
            print(f"   Заблокированные: {', '.join(blocked_topics[:3])}")
        if available_topics:
            print(f"   Доступные: {', '.join(available_topics[:3])}")
        
        # ШАГ 5: Отправка аналитического отчета
        print("\n📊 ШАГ 5: Аналитический отчет")
        print("-" * 70)
        
        notifier.send_analytics_report(analytics, days=7)
        
        # ШАГ 6: Проверка статистики уведомлений
        print("\n📱 ШАГ 6: Статистика уведомлений")
        print("-" * 70)
        
        notif_stats = notifier.get_notification_stats()
        print(f"   Всего уведомлений: {notif_stats['total']}")
        print(f"   Запусков: {notif_stats['startup']}")
        print(f"   Ошибок: {notif_stats['errors']}")
        print(f"   Успехов: {notif_stats['success']}")
        print(f"   Отчетов: {notif_stats['analytics']}")
        
        # ШАГ 7: Финальная проверка
        print("\n✅ ШАГ 7: Финальная проверка")
        print("-" * 70)
        
        # Проверяем, что все работает корректно
        checks = {
            'БД создана': os.path.exists(test_db_path),
            'Посты сохранены': total_posts == 10,
            'Темы использованы': len(distribution) > 0,
            'Дедупликация работает': len(blocked_topics) > 0,
            'Уведомления отправлены': notif_stats['total'] > 0,
            'Лог создан': os.path.exists(log_file)
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            if not result:
                all_passed = False
        
        # Итоговый результат
        print("\n" + "=" * 70)
        if all_passed:
            print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("=" * 70)
            print("\n🎉 Система полностью функциональна и готова к работе!")
        else:
            print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
            print("=" * 70)
        
        return all_passed
        
    finally:
        # Очистка
        if 'db' in locals():
            db.close()
        
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("\n🗑️  Тестовая БД удалена")


if __name__ == '__main__':
    success = test_complete_workflow()
    exit(0 if success else 1)
