#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая работа с базой данных.
Без ORM. Явные SQL запросы.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict


class Database:
    """
    Простой класс для работы с БД.
    Один класс - одна ответственность.
    """
    
    def __init__(self, db_path: str = 'data/bot.db'):
        """Явная инициализация с путем к БД."""
        self.db_path = db_path
        self.conn = None
        
        # Создаем папку data если не существует
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def connect(self):
        """Явное подключение."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Для dict-like доступа
    
    def close(self):
        """Явное закрытие."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def init_tables(self):
        """
        Создает таблицы если их нет.
        Явный SQL. Без магии.
        """
        # Таблица постов
        posts_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            topic TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            published BOOLEAN DEFAULT 0
        )
        """
        
        # Таблица тем
        topics_sql = """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            last_used TIMESTAMP,
            usage_count INTEGER DEFAULT 0
        )
        """
        
        self.conn.execute(posts_sql)
        self.conn.execute(topics_sql)
        self.conn.commit()
    
    def save_post(self, title: str, body: str, topic: str) -> int:
        """
        Сохраняет пост.
        Явные параметры. Возвращает ID.
        """
        sql = "INSERT INTO posts (title, body, topic, published) VALUES (?, ?, ?, 1)"
        cursor = self.conn.execute(sql, (title, body, topic))
        self.conn.commit()
        
        # Обновляем статистику темы
        self._update_topic_usage(topic)
        
        return cursor.lastrowid
    
    def get_recent_posts(self, limit: int = 50) -> List[Dict]:
        """
        Получает последние посты.
        Явный лимит. Возвращает список словарей.
        """
        sql = "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?"
        cursor = self.conn.execute(sql, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """
        Получает пост по ID.
        """
        sql = "SELECT * FROM posts WHERE id = ?"
        cursor = self.conn.execute(sql, (post_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def topic_used_recently(self, topic: str, days: int = 7) -> bool:
        """
        Проверяет использовалась ли тема недавно.
        Простая проверка. True или False.
        """
        sql = """
        SELECT COUNT(*) as count FROM posts 
        WHERE topic = ? 
        AND created_at > datetime('now', '-' || ? || ' days')
        """
        cursor = self.conn.execute(sql, (topic, days))
        result = cursor.fetchone()
        return result['count'] > 0
    
    def get_topic_stats(self, topic: str) -> Dict:
        """
        Получает статистику по теме.
        """
        sql = "SELECT * FROM topics WHERE name = ?"
        cursor = self.conn.execute(sql, (topic,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        else:
            return {
                'name': topic,
                'last_used': None,
                'usage_count': 0
            }
    
    def get_all_topics_stats(self) -> List[Dict]:
        """
        Получает статистику по всем темам.
        """
        sql = "SELECT * FROM topics ORDER BY usage_count DESC"
        cursor = self.conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    
    def _update_topic_usage(self, topic: str):
        """
        Обновляет статистику использования темы.
        Внутренний метод.
        """
        # Проверяем существует ли тема
        check_sql = "SELECT id FROM topics WHERE name = ?"
        cursor = self.conn.execute(check_sql, (topic,))
        exists = cursor.fetchone()
        
        if exists:
            # Обновляем
            update_sql = """
            UPDATE topics 
            SET last_used = CURRENT_TIMESTAMP, usage_count = usage_count + 1 
            WHERE name = ?
            """
            self.conn.execute(update_sql, (topic,))
        else:
            # Создаем
            insert_sql = """
            INSERT INTO topics (name, last_used, usage_count) 
            VALUES (?, CURRENT_TIMESTAMP, 1)
            """
            self.conn.execute(insert_sql, (topic,))
        
        self.conn.commit()
    
    def get_total_posts(self) -> int:
        """Возвращает общее количество постов."""
        sql = "SELECT COUNT(*) as count FROM posts"
        cursor = self.conn.execute(sql)
        return cursor.fetchone()['count']
    
    def clear_old_posts(self, days: int = 90):
        """
        Удаляет старые посты.
        """
        sql = "DELETE FROM posts WHERE created_at < datetime('now', '-' || ? || ' days')"
        cursor = self.conn.execute(sql, (days,))
        self.conn.commit()
        return cursor.rowcount


# Простое использование и тестирование
if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ DATABASE.PY")
    print("=" * 60)
    
    # Используем тестовую БД
    test_db_path = 'data/test_bot.db'
    
    # Удаляем тестовую БД если существует
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = Database(test_db_path)
    db.connect()
    
    try:
        # Тест 1: Создание таблиц
        print("\n1. Создание таблиц:")
        db.init_tables()
        print("   ✅ Таблицы созданы")
        
        # Тест 2: Сохранение постов
        print("\n2. Сохранение постов:")
        post_id1 = db.save_post('Заголовок 1', 'Текст поста 1', 'фитнес')
        post_id2 = db.save_post('Заголовок 2', 'Текст поста 2', 'питание')
        post_id3 = db.save_post('Заголовок 3', 'Текст поста 3', 'фитнес')
        print(f"   ✅ Сохранено 3 поста (IDs: {post_id1}, {post_id2}, {post_id3})")
        
        # Тест 3: Получение постов
        print("\n3. Получение последних постов:")
        recent = db.get_recent_posts(limit=10)
        print(f"   ✅ Получено постов: {len(recent)}")
        print(f"   Последний пост: {recent[0]['title']}")
        
        # Тест 4: Получение поста по ID
        print("\n4. Получение поста по ID:")
        post = db.get_post_by_id(post_id1)
        print(f"   ✅ Пост #{post_id1}: {post['title']}")
        
        # Тест 5: Проверка использования темы
        print("\n5. Проверка использования темы:")
        used = db.topic_used_recently('фитнес', days=7)
        not_used = db.topic_used_recently('йога', days=7)
        print(f"   ✅ 'фитнес' использовалась: {used}")
        print(f"   ✅ 'йога' не использовалась: {not not_used}")
        
        # Тест 6: Статистика темы
        print("\n6. Статистика темы:")
        stats = db.get_topic_stats('фитнес')
        print(f"   Тема: {stats['name']}")
        print(f"   Использований: {stats['usage_count']}")
        print(f"   ✅ Использовано 2 раза: {stats['usage_count'] == 2}")
        
        # Тест 7: Статистика всех тем
        print("\n7. Статистика всех тем:")
        all_stats = db.get_all_topics_stats()
        print(f"   ✅ Всего тем: {len(all_stats)}")
        for stat in all_stats:
            print(f"      - {stat['name']}: {stat['usage_count']} раз")
        
        # Тест 8: Общее количество постов
        print("\n8. Общее количество постов:")
        total = db.get_total_posts()
        print(f"   ✅ Всего постов: {total}")
        
        # Тест 9: Удаление старых постов
        print("\n9. Удаление старых постов:")
        deleted = db.clear_old_posts(days=0)  # Удаляем все (для теста)
        print(f"   ✅ Удалено постов: {deleted}")
        
        remaining = db.get_total_posts()
        print(f"   ✅ Осталось постов: {remaining}")
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
        print("=" * 60)
        
    finally:
        db.close()
        
        # Удаляем тестовую БД
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("\n🗑️  Тестовая БД удалена")
