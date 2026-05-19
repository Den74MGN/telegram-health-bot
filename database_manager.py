#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль управления базой данных для постов.
Хранит историю публикаций, аналитику и темы.
"""

import sqlite3
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Менеджер базы данных для хранения постов и аналитики.
    """
    
    def __init__(self, db_path: str = 'data/bot.db'):
        """
        Инициализация менеджера БД.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.conn = None
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для безопасной работы с БД."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Доступ к колонкам по имени
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Ошибка БД: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Создание таблиц базы данных."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Таблица постов
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        topic TEXT NOT NULL,
                        hashtags TEXT,
                        seo_keywords TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        published_at TIMESTAMP,
                        views INTEGER DEFAULT 0,
                        reactions INTEGER DEFAULT 0,
                        shares INTEGER DEFAULT 0,
                        image_generated BOOLEAN DEFAULT 0,
                        status TEXT DEFAULT 'published'
                    )
                ''')
                
                # Таблица тем
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        last_used TIMESTAMP,
                        usage_count INTEGER DEFAULT 0,
                        avg_views REAL DEFAULT 0,
                        avg_reactions REAL DEFAULT 0,
                        priority INTEGER DEFAULT 0
                    )
                ''')
                
                # Таблица аналитики
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        post_id INTEGER,
                        metric_name TEXT NOT NULL,
                        metric_value REAL NOT NULL,
                        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (post_id) REFERENCES posts (id)
                    )
                ''')
                
                # Индексы для быстрого поиска
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_posts_topic 
                    ON posts(topic)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_posts_published_at 
                    ON posts(published_at)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_topics_last_used 
                    ON topics(last_used)
                ''')
                
                logger.info("База данных инициализирована успешно")
                
        except Exception as e:
            logger.error(f"Ошибка инициализации БД: {e}")
            raise
    
    def save_post(self, post_data: Dict) -> int:
        """
        Сохранение поста в базу данных.
        
        Args:
            post_data: Словарь с данными поста
            
        Returns:
            int: ID сохраненного поста
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Конвертируем списки в JSON строки
                hashtags = json.dumps(post_data.get('hashtags', []))
                seo_keywords = json.dumps(post_data.get('seo_keywords', []))
                
                cursor.execute('''
                    INSERT INTO posts (
                        title, body, topic, hashtags, seo_keywords,
                        published_at, image_generated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    post_data.get('title'),
                    post_data.get('body'),
                    post_data.get('topic'),
                    hashtags,
                    seo_keywords,
                    datetime.now().isoformat(),
                    bool(post_data.get('image_bytes'))
                ))
                
                post_id = cursor.lastrowid
                
                # Обновляем статистику темы в том же соединении
                self._update_topic_usage(post_data.get('topic'), conn)
                
                logger.info(f"Пост сохранен с ID: {post_id}")
                return post_id
                
        except Exception as e:
            logger.error(f"Ошибка сохранения поста: {e}")
            raise
    
    def _update_topic_usage(self, topic: str, conn=None):
        """Обновление статистики использования темы."""
        try:
            # Используем переданное соединение или создаем новое
            if conn is None:
                with self.get_connection() as conn:
                    self._do_update_topic(conn, topic)
            else:
                self._do_update_topic(conn, topic)
                    
        except Exception as e:
            logger.error(f"Ошибка обновления темы: {e}")
    
    def _do_update_topic(self, conn, topic: str):
        """Внутренний метод обновления темы."""
        cursor = conn.cursor()
        
        # Проверяем существование темы
        cursor.execute('SELECT id FROM topics WHERE name = ?', (topic,))
        result = cursor.fetchone()
        
        if result:
            # Обновляем существующую тему
            cursor.execute('''
                UPDATE topics 
                SET last_used = ?, usage_count = usage_count + 1
                WHERE name = ?
            ''', (datetime.now().isoformat(), topic))
        else:
            # Создаем новую тему
            cursor.execute('''
                INSERT INTO topics (name, last_used, usage_count)
                VALUES (?, ?, 1)
            ''', (topic, datetime.now().isoformat()))
    
    def get_recent_posts(self, limit: int = 50) -> List[Dict]:
        """
        Получение последних постов.
        
        Args:
            limit: Количество постов
            
        Returns:
            List[Dict]: Список постов
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM posts 
                    ORDER BY published_at DESC 
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                
                posts = []
                for row in rows:
                    post = dict(row)
                    # Конвертируем JSON строки обратно в списки
                    post['hashtags'] = json.loads(post['hashtags']) if post['hashtags'] else []
                    post['seo_keywords'] = json.loads(post['seo_keywords']) if post['seo_keywords'] else []
                    posts.append(post)
                
                return posts
                
        except Exception as e:
            logger.error(f"Ошибка получения постов: {e}")
            return []
    
    def check_topic_availability(self, topic: str, block_days: int = 7) -> bool:
        """
        Проверка доступности темы (не использовалась последние N дней).
        
        Args:
            topic: Название темы
            block_days: Количество дней блокировки
            
        Returns:
            bool: True если тема доступна
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                block_date = (datetime.now() - timedelta(days=block_days)).isoformat()
                
                cursor.execute('''
                    SELECT last_used FROM topics 
                    WHERE name = ? AND last_used > ?
                ''', (topic, block_date))
                
                result = cursor.fetchone()
                
                # Тема доступна если не найдена или использовалась давно
                return result is None
                
        except Exception as e:
            logger.error(f"Ошибка проверки темы: {e}")
            return True  # В случае ошибки разрешаем использование
    
    def get_topic_statistics(self) -> List[Dict]:
        """
        Получение статистики по темам.
        
        Returns:
            List[Dict]: Статистика тем
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        t.name,
                        t.usage_count,
                        t.last_used,
                        AVG(p.views) as avg_views,
                        AVG(p.reactions) as avg_reactions
                    FROM topics t
                    LEFT JOIN posts p ON t.name = p.topic
                    GROUP BY t.name
                    ORDER BY t.usage_count DESC
                ''')
                
                rows = cursor.fetchall()
                
                stats = []
                for row in rows:
                    stats.append({
                        'name': row['name'],
                        'usage_count': row['usage_count'],
                        'last_used': row['last_used'],
                        'avg_views': row['avg_views'] or 0,
                        'avg_reactions': row['avg_reactions'] or 0
                    })
                
                return stats
                
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return []
    
    def get_available_topics(self, all_topics: List[str], block_days: int = 7) -> List[str]:
        """
        Получение списка доступных тем.
        
        Args:
            all_topics: Полный список тем
            block_days: Количество дней блокировки
            
        Returns:
            List[str]: Доступные темы
        """
        available = []
        for topic in all_topics:
            if self.check_topic_availability(topic, block_days):
                available.append(topic)
        
        return available if available else all_topics  # Если все заблокированы, возвращаем все
    
    def update_post_metrics(self, post_id: int, views: int = 0, reactions: int = 0, shares: int = 0):
        """
        Обновление метрик поста.
        
        Args:
            post_id: ID поста
            views: Количество просмотров
            reactions: Количество реакций
            shares: Количество репостов
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE posts 
                    SET views = ?, reactions = ?, shares = ?
                    WHERE id = ?
                ''', (views, reactions, shares, post_id))
                
                logger.info(f"Метрики поста {post_id} обновлены")
                
        except Exception as e:
            logger.error(f"Ошибка обновления метрик: {e}")
    
    def get_total_posts(self) -> int:
        """Получение общего количества постов."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) as count FROM posts')
                result = cursor.fetchone()
                return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Ошибка подсчета постов: {e}")
            return 0
    
    def backup_database(self, backup_path: str = None):
        """
        Создание резервной копии базы данных.
        
        Args:
            backup_path: Путь для сохранения бэкапа
        """
        try:
            if backup_path is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f'backups/bot_db_backup_{timestamp}.db'
            
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Копируем файл БД
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"Резервная копия создана: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Ошибка создания бэкапа: {e}")
            return None


# Тестирование модуля
if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ DATABASE_MANAGER")
    print("=" * 60)
    
    # Создаем тестовую БД
    test_db_path = 'data/test_bot.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = DatabaseManager(test_db_path)
    
    # Тест 1: Инициализация
    print("\n1. Инициализация БД...")
    db.init_database()
    print("   ✅ БД инициализирована")
    
    # Тест 2: Сохранение постов
    print("\n2. Сохранение постов...")
    test_posts = [
        {
            'title': 'Тест 1: Здоровое питание',
            'body': 'Текст о здоровом питании',
            'topic': 'здоровое питание',
            'hashtags': ['#здоровье', '#питание'],
            'seo_keywords': ['здоровье', 'питание'],
            'image_bytes': b'test'
        },
        {
            'title': 'Тест 2: Фитнес',
            'body': 'Текст о фитнесе',
            'topic': 'фитнес упражнения',
            'hashtags': ['#фитнес', '#спорт'],
            'seo_keywords': ['фитнес', 'спорт']
        },
        {
            'title': 'Тест 3: Здоровое питание снова',
            'body': 'Еще текст о питании',
            'topic': 'здоровое питание',
            'hashtags': ['#здоровье'],
            'seo_keywords': ['здоровье']
        }
    ]
    
    post_ids = []
    for post in test_posts:
        post_id = db.save_post(post)
        post_ids.append(post_id)
        print(f"   ✅ Пост сохранен с ID: {post_id}")
    
    # Тест 3: Получение постов
    print("\n3. Получение последних постов...")
    recent_posts = db.get_recent_posts(limit=10)
    print(f"   Получено постов: {len(recent_posts)}")
    for post in recent_posts:
        print(f"   - {post['title']} (тема: {post['topic']})")
    print("   ✅ Посты получены")
    
    # Тест 4: Проверка доступности темы
    print("\n4. Проверка доступности тем...")
    topics = ['здоровое питание', 'фитнес упражнения', 'йога']
    for topic in topics:
        available = db.check_topic_availability(topic, block_days=7)
        status = "доступна" if available else "заблокирована"
        print(f"   - {topic}: {status}")
    print("   ✅ Проверка выполнена")
    
    # Тест 5: Статистика тем
    print("\n5. Статистика тем...")
    stats = db.get_topic_statistics()
    for stat in stats:
        print(f"   - {stat['name']}: использований {stat['usage_count']}")
    print("   ✅ Статистика получена")
    
    # Тест 6: Доступные темы
    print("\n6. Получение доступных тем...")
    all_topics = ['здоровое питание', 'фитнес упражнения', 'йога', 'медитация']
    available_topics = db.get_available_topics(all_topics, block_days=7)
    print(f"   Доступно тем: {len(available_topics)}")
    print(f"   Темы: {', '.join(available_topics)}")
    print("   ✅ Доступные темы получены")
    
    # Тест 7: Обновление метрик
    print("\n7. Обновление метрик поста...")
    db.update_post_metrics(post_ids[0], views=100, reactions=10, shares=5)
    print("   ✅ Метрики обновлены")
    
    # Тест 8: Общее количество
    print("\n8. Подсчет постов...")
    total = db.get_total_posts()
    print(f"   Всего постов: {total}")
    print("   ✅ Подсчет выполнен")
    
    # Тест 9: Резервная копия
    print("\n9. Создание резервной копии...")
    backup_path = db.backup_database()
    if backup_path:
        print(f"   ✅ Бэкап создан: {backup_path}")
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 60)
    
    # Удаляем тестовую БД
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print("\n🗑️  Тестовая БД удалена")
