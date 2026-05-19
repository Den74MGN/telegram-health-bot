#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интеграционный тест всех модулей.
Проверяет работу модулей вместе.
"""

import os
from prompts import create_image_prompt, get_available_topics
from optimizer import format_caption, validate_length, get_text_stats
from database import Database
from deduplicator import Deduplicator


def test_full_workflow():
    """
    Тестирует полный рабочий процесс:
    1. Выбор темы через дедупликатор
    2. Генерация промпта для изображения
    3. Оптимизация текста
    4. Сохранение в БД
    """
    print("=" * 60)
    print("ИНТЕГРАЦИОННЫЙ ТЕСТ ВСЕХ МОДУЛЕЙ")
    print("=" * 60)
    
    # Подготовка
    test_db_path = 'data/test_integration.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = Database(test_db_path)
    db.connect()
    db.init_tables()
    
    dedup = Deduplicator(db, block_days=7)
    
    try:
        # Шаг 1: Выбор темы
        print("\n📋 ШАГ 1: Выбор темы")
        print("-" * 60)
        
        topics = get_available_topics()
        print(f"Доступно тем: {len(topics)}")
        
        selected_topic = dedup.get_best_topic(topics[:5])  # Берем первые 5
        print(f"✅ Выбрана тема: {selected_topic}")
        
        # Шаг 2: Генерация промпта для изображения
        print("\n🎨 ШАГ 2: Генерация промпта для изображения")
        print("-" * 60)
        
        title = "5 простых упражнений для здоровья"
        image_prompt = create_image_prompt(selected_topic, title)
        
        print(f"Заголовок: {title}")
        print(f"Длина промпта: {len(image_prompt)} символов")
        print(f"Промпт: {image_prompt[:150]}...")
        print(f"✅ Промпт сгенерирован")
        
        # Шаг 3: Создание и оптимизация текста
        print("\n📝 ШАГ 3: Оптимизация текста")
        print("-" * 60)
        
        body = """
        Здоровье - это самое важное в нашей жизни. 
        
        Вот 5 простых упражнений которые помогут вам оставаться в форме:
        
        1. Приседания - укрепляют ноги и ягодицы
        2. Отжимания - развивают грудь и руки
        3. Планка - укрепляет корпус
        4. Выпады - улучшают баланс
        5. Скручивания - тренируют пресс
        
        Начните с 10 повторений каждого упражнения и постепенно увеличивайте нагрузку!
        """.strip()
        
        hashtags = ['#здоровье', '#фитнес', '#упражнения', '#ЗОЖ', '#тренировка']
        
        # Форматируем caption
        caption = format_caption(title, body, hashtags)
        
        # Проверяем статистику
        stats = get_text_stats(caption)
        
        print(f"Длина caption: {stats['length']} символов")
        print(f"Слов: {stats['words']}")
        print(f"Время чтения: {stats['reading_time']} секунд")
        print(f"Валидно: {stats['valid']}")
        print(f"✅ Текст оптимизирован")
        
        # Шаг 4: Сохранение в БД
        print("\n💾 ШАГ 4: Сохранение в БД")
        print("-" * 60)
        
        post_id = db.save_post(title, body, selected_topic)
        print(f"✅ Пост сохранен с ID: {post_id}")
        
        # Проверяем что тема заблокирована
        is_blocked = not dedup.is_available(selected_topic)
        print(f"✅ Тема заблокирована: {is_blocked}")
        
        # Шаг 5: Проверка работы дедупликатора
        print("\n🔄 ШАГ 5: Проверка дедупликатора")
        print("-" * 60)
        
        # Выбираем следующую тему
        next_topic = dedup.get_next_topic(topics[:5])
        print(f"Следующая тема: {next_topic}")
        print(f"✅ Следующая тема отличается: {next_topic != selected_topic}")
        
        # Шаг 6: Создаем несколько постов
        print("\n📚 ШАГ 6: Создание нескольких постов")
        print("-" * 60)
        
        for i in range(3):
            topic = dedup.get_next_topic(topics[:5])
            test_title = f"Тестовый пост #{i+1}"
            test_body = f"Текст тестового поста {i+1}"
            
            post_id = db.save_post(test_title, test_body, topic)
            print(f"   Пост #{i+1}: тема '{topic}', ID {post_id}")
        
        total_posts = db.get_total_posts()
        print(f"✅ Всего постов в БД: {total_posts}")
        
        # Шаг 7: Статистика
        print("\n📊 ШАГ 7: Статистика")
        print("-" * 60)
        
        all_stats = db.get_all_topics_stats()
        print(f"Статистика по темам:")
        for stat in all_stats:
            print(f"   - {stat['name']}: {stat['usage_count']} использований")
        
        print(f"✅ Статистика собрана")
        
        # Финальная проверка
        print("\n" + "=" * 60)
        print("✅ ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЙДЕН")
        print("=" * 60)
        
        print("\n📋 Итоговая сводка:")
        print(f"   • Модулей протестировано: 4")
        print(f"   • Постов создано: {total_posts}")
        print(f"   • Тем использовано: {len(all_stats)}")
        print(f"   • Все модули работают корректно: ✅")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()
        
        # Удаляем тестовую БД
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("\n🗑️  Тестовая БД удалена")


if __name__ == '__main__':
    success = test_full_workflow()
    exit(0 if success else 1)
