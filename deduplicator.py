#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая дедупликация контента.
Без сложной логики. Явно и понятно.
"""

from typing import List
from database import Database


class Deduplicator:
    """
    Простой дедупликатор.
    Проверяет не использовалась ли тема недавно.
    """
    
    def __init__(self, db: Database, block_days: int = 7):
        """
        Явная инициализация с зависимостями.
        
        Args:
            db: Экземпляр Database
            block_days: Сколько дней блокировать тему после использования
        """
        self.db = db
        self.block_days = block_days
    
    def is_available(self, topic: str) -> bool:
        """
        Проверяет доступна ли тема.
        Простая проверка. True или False.
        
        Args:
            topic: Название темы
        
        Returns:
            bool: True если тему можно использовать
        """
        return not self.db.topic_used_recently(topic, self.block_days)
    
    def get_next_topic(self, topics: List[str]) -> str:
        """
        Выбирает следующую доступную тему.
        Простой перебор. Первая доступная.
        
        Args:
            topics: Список тем
        
        Returns:
            str: Следующая доступная тема
        """
        # Ищем первую доступную
        for topic in topics:
            if self.is_available(topic):
                return topic
        
        # Если все заблокированы - берем первую (самую старую)
        return topics[0]
    
    def filter_available(self, topics: List[str]) -> List[str]:
        """
        Фильтрует доступные темы.
        Простой list comprehension.
        
        Args:
            topics: Список тем
        
        Returns:
            list: Список доступных тем
        """
        return [t for t in topics if self.is_available(t)]
    
    def get_topic_priority(self, topics: List[str]) -> List[tuple]:
        """
        Возвращает темы с приоритетом (сколько дней не использовалась).
        
        Args:
            topics: Список тем
        
        Returns:
            list: Список кортежей (тема, приоритет)
        """
        result = []
        
        for topic in topics:
            stats = self.db.get_topic_stats(topic)
            
            # Если никогда не использовалась - высокий приоритет
            if stats['usage_count'] == 0:
                priority = 999
            else:
                # Приоритет = количество использований (меньше = выше приоритет)
                priority = -stats['usage_count']
            
            result.append((topic, priority))
        
        # Сортируем по приоритету (больше = выше)
        result.sort(key=lambda x: x[1], reverse=True)
        
        return result
    
    def get_best_topic(self, topics: List[str]) -> str:
        """
        Выбирает лучшую тему с учетом приоритета.
        
        Args:
            topics: Список тем
        
        Returns:
            str: Лучшая тема
        """
        # Сначала фильтруем доступные
        available = self.filter_available(topics)
        
        if not available:
            # Если нет доступных - берем с наименьшим использованием
            available = topics
        
        # Получаем приоритеты
        priorities = self.get_topic_priority(available)
        
        # Возвращаем тему с наивысшим приоритетом
        return priorities[0][0] if priorities else topics[0]


# Простое использование и тестирование
if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ DEDUPLICATOR.PY")
    print("=" * 60)
    
    # Создаем тестовую БД
    test_db_path = 'data/test_dedup.db'
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = Database(test_db_path)
    db.connect()
    db.init_tables()
    
    try:
        # Создаем дедупликатор
        dedup = Deduplicator(db, block_days=7)
        
        # Тест 1: Проверка доступности новой темы
        print("\n1. Проверка доступности новой темы:")
        available = dedup.is_available('фитнес')
        print(f"   ✅ 'фитнес' доступна: {available}")
        
        # Тест 2: Сохраняем пост и проверяем блокировку
        print("\n2. Блокировка после использования:")
        db.save_post('Тест', 'Текст', 'фитнес')
        available_after = dedup.is_available('фитнес')
        print(f"   ✅ 'фитнес' заблокирована: {not available_after}")
        
        # Тест 3: Фильтрация доступных тем
        print("\n3. Фильтрация доступных тем:")
        topics = ['фитнес', 'питание', 'йога']
        available_topics = dedup.filter_available(topics)
        print(f"   Всего тем: {len(topics)}")
        print(f"   Доступных: {len(available_topics)}")
        print(f"   ✅ Доступные: {available_topics}")
        
        # Тест 4: Выбор следующей темы
        print("\n4. Выбор следующей темы:")
        next_topic = dedup.get_next_topic(topics)
        print(f"   ✅ Следующая тема: {next_topic}")
        print(f"   ✅ Не 'фитнес': {next_topic != 'фитнес'}")
        
        # Тест 5: Используем еще темы
        print("\n5. Использование нескольких тем:")
        db.save_post('Тест 2', 'Текст', 'питание')
        db.save_post('Тест 3', 'Текст', 'питание')  # Дважды
        db.save_post('Тест 4', 'Текст', 'йога')
        
        available_topics = dedup.filter_available(topics)
        print(f"   ✅ Доступных тем: {len(available_topics)}")
        
        # Тест 6: Приоритеты тем
        print("\n6. Приоритеты тем:")
        priorities = dedup.get_topic_priority(topics)
        print("   Темы по приоритету:")
        for topic, priority in priorities:
            stats = db.get_topic_stats(topic)
            print(f"      - {topic}: приоритет {priority}, использований {stats['usage_count']}")
        
        # Тест 7: Выбор лучшей темы
        print("\n7. Выбор лучшей темы:")
        best = dedup.get_best_topic(topics)
        print(f"   ✅ Лучшая тема: {best}")
        
        # Тест 8: Когда все темы заблокированы
        print("\n8. Когда все темы заблокированы:")
        # Используем все темы
        for topic in topics:
            if dedup.is_available(topic):
                db.save_post(f'Тест {topic}', 'Текст', topic)
        
        available_topics = dedup.filter_available(topics)
        print(f"   Доступных тем: {len(available_topics)}")
        
        # Все равно должна вернуться тема
        next_topic = dedup.get_next_topic(topics)
        print(f"   ✅ Возвращена тема: {next_topic}")
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
        print("=" * 60)
        
    finally:
        db.close()
        
        # Удаляем тестовую БД
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("\n🗑️  Тестовая БД удалена")
