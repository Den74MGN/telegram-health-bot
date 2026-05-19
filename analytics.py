#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая аналитика контента.
Анализ эффективности постов и тем.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from database import Database


class Analytics:
    """
    Простой класс аналитики.
    Анализирует эффективность контента.
    """
    
    def __init__(self, db: Database):
        """
        Явная инициализация с БД.
        
        Args:
            db: Экземпляр Database
        """
        self.db = db
    
    def get_total_posts(self) -> int:
        """Возвращает общее количество постов."""
        return self.db.get_total_posts()
    
    def get_posts_by_period(self, days: int = 7) -> List[Dict]:
        """
        Получает посты за период.
        
        Args:
            days: Количество дней
        
        Returns:
            list: Список постов
        """
        all_posts = self.db.get_recent_posts(limit=1000)
        
        # Фильтруем по дате
        cutoff_date = datetime.now() - timedelta(days=days)
        
        result = []
        for post in all_posts:
            post_date = datetime.fromisoformat(post['created_at'])
            if post_date >= cutoff_date:
                result.append(post)
        
        return result
    
    def get_top_topics(self, limit: int = 5) -> List[Dict]:
        """
        Возвращает топ тем по использованию.
        
        Args:
            limit: Количество тем
        
        Returns:
            list: Список тем с статистикой
        """
        all_stats = self.db.get_all_topics_stats()
        return all_stats[:limit]
    
    def get_topic_distribution(self) -> Dict[str, int]:
        """
        Возвращает распределение постов по темам.
        
        Returns:
            dict: {тема: количество}
        """
        all_stats = self.db.get_all_topics_stats()
        return {stat['name']: stat['usage_count'] for stat in all_stats}
    
    def get_posting_frequency(self, days: int = 7) -> float:
        """
        Вычисляет частоту публикаций (постов в день).
        
        Args:
            days: Период для анализа
        
        Returns:
            float: Постов в день
        """
        posts = self.get_posts_by_period(days)
        
        if not posts or days == 0:
            return 0.0
        
        return len(posts) / days
    
    def get_summary(self, days: int = 7) -> Dict:
        """
        Возвращает сводку по аналитике.
        
        Args:
            days: Период для анализа
        
        Returns:
            dict: Сводка с метриками
        """
        posts = self.get_posts_by_period(days)
        top_topics = self.get_top_topics(limit=5)
        frequency = self.get_posting_frequency(days)
        
        return {
            'period_days': days,
            'total_posts': self.get_total_posts(),
            'posts_in_period': len(posts),
            'posting_frequency': round(frequency, 2),
            'top_topics': [t['name'] for t in top_topics],
            'topic_distribution': self.get_topic_distribution()
        }
    
    def generate_report(self, days: int = 7) -> str:
        """
        Генерирует текстовый отчет.
        
        Args:
            days: Период для анализа
        
        Returns:
            str: Текстовый отчет
        """
        summary = self.get_summary(days)
        
        report = f"""
📊 ОТЧЕТ ПО АНАЛИТИКЕ
{'=' * 60}

📅 Период: последние {days} дней
📝 Всего постов: {summary['total_posts']}
📈 Постов за период: {summary['posts_in_period']}
⏱️ Частота публикаций: {summary['posting_frequency']} постов/день

🏆 ТОП-5 ТЕМ:
"""
        
        for i, topic in enumerate(summary['top_topics'], 1):
            count = summary['topic_distribution'].get(topic, 0)
            report += f"\n   {i}. {topic}: {count} постов"
        
        report += f"\n\n📊 РАСПРЕДЕЛЕНИЕ ПО ТЕМАМ:\n"
        
        for topic, count in summary['topic_distribution'].items():
            percentage = (count / summary['total_posts'] * 100) if summary['total_posts'] > 0 else 0
            report += f"\n   • {topic}: {count} ({percentage:.1f}%)"
        
        report += f"\n\n{'=' * 60}"
        
        return report.strip()
    
    def get_least_used_topics(self, topics: List[str]) -> List[str]:
        """
        Возвращает наименее используемые темы.
        
        Args:
            topics: Список тем для проверки
        
        Returns:
            list: Темы отсортированные по использованию (меньше = первые)
        """
        distribution = self.get_topic_distribution()
        
        # Сортируем темы по использованию
        sorted_topics = sorted(
            topics,
            key=lambda t: distribution.get(t, 0)
        )
        
        return sorted_topics


# Простое использование и тестирование
if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ ANALYTICS.PY")
    print("=" * 60)
    
    # Создаем тестовую БД с данными
    test_db_path = 'data/test_analytics.db'
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = Database(test_db_path)
    db.connect()
    db.init_tables()
    
    try:
        # Создаем тестовые данные
        print("\n📝 Создание тестовых данных...")
        
        test_posts = [
            ('Пост 1', 'Текст 1', 'фитнес'),
            ('Пост 2', 'Текст 2', 'питание'),
            ('Пост 3', 'Текст 3', 'фитнес'),
            ('Пост 4', 'Текст 4', 'йога'),
            ('Пост 5', 'Текст 5', 'питание'),
            ('Пост 6', 'Текст 6', 'фитнес'),
        ]
        
        for title, body, topic in test_posts:
            db.save_post(title, body, topic)
        
        print(f"   ✅ Создано {len(test_posts)} тестовых постов")
        
        # Создаем аналитику
        analytics = Analytics(db)
        
        # Тест 1: Общее количество постов
        print("\n1. Общее количество постов:")
        total = analytics.get_total_posts()
        print(f"   ✅ Всего постов: {total}")
        
        # Тест 2: Посты за период
        print("\n2. Посты за последние 7 дней:")
        recent = analytics.get_posts_by_period(days=7)
        print(f"   ✅ Постов за период: {len(recent)}")
        
        # Тест 3: Топ тем
        print("\n3. Топ-5 тем:")
        top_topics = analytics.get_top_topics(limit=5)
        for i, topic in enumerate(top_topics, 1):
            print(f"   {i}. {topic['name']}: {topic['usage_count']} постов")
        print(f"   ✅ Топ тем получен")
        
        # Тест 4: Распределение по темам
        print("\n4. Распределение по темам:")
        distribution = analytics.get_topic_distribution()
        for topic, count in distribution.items():
            print(f"   • {topic}: {count}")
        print(f"   ✅ Распределение получено")
        
        # Тест 5: Частота публикаций
        print("\n5. Частота публикаций:")
        frequency = analytics.get_posting_frequency(days=7)
        print(f"   ✅ Частота: {frequency} постов/день")
        
        # Тест 6: Сводка
        print("\n6. Сводка по аналитике:")
        summary = analytics.get_summary(days=7)
        print(f"   Период: {summary['period_days']} дней")
        print(f"   Всего постов: {summary['total_posts']}")
        print(f"   Постов за период: {summary['posts_in_period']}")
        print(f"   Частота: {summary['posting_frequency']} постов/день")
        print(f"   Топ тем: {', '.join(summary['top_topics'][:3])}")
        print(f"   ✅ Сводка получена")
        
        # Тест 7: Генерация отчета
        print("\n7. Генерация текстового отчета:")
        report = analytics.generate_report(days=7)
        print(report)
        print(f"\n   ✅ Отчет сгенерирован")
        
        # Тест 8: Наименее используемые темы
        print("\n8. Наименее используемые темы:")
        all_topics = ['фитнес', 'питание', 'йога', 'сон', 'стресс']
        least_used = analytics.get_least_used_topics(all_topics)
        print(f"   Темы по возрастанию использования:")
        for topic in least_used:
            count = distribution.get(topic, 0)
            print(f"      - {topic}: {count} постов")
        print(f"   ✅ Наименее используемые определены")
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
        print("=" * 60)
        
    finally:
        db.close()
        
        # Удаляем тестовую БД
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("\n🗑️  Тестовая БД удалена")
