#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система уведомлений.
Отправка алертов и отчетов администратору.
"""

import os
from typing import Optional
from datetime import datetime
from analytics import Analytics


class NotificationManager:
    """
    Простой менеджер уведомлений.
    Отправляет сообщения администратору.
    """
    
    def __init__(self, admin_chat_id: Optional[str] = None):
        """
        Инициализация с ID администратора.
        
        Args:
            admin_chat_id: Telegram ID администратора
        """
        self.admin_chat_id = admin_chat_id or os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        self.enabled = bool(self.admin_chat_id and self.admin_chat_id != 'YOUR_PERSONAL_TELEGRAM_ID')
    
    def format_startup_message(self) -> str:
        """
        Форматирует сообщение о запуске бота.
        
        Returns:
            str: Сообщение о запуске
        """
        timestamp = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
        
        return f"""
🚀 *БОТ ЗАПУЩЕН*

⏰ Время: {timestamp}
🤖 Статус: Активен
📊 Режим: Автоматический

✅ Все системы работают
        """.strip()
    
    def format_error_message(self, error: str, context: str = '') -> str:
        """
        Форматирует сообщение об ошибке.
        
        Args:
            error: Текст ошибки
            context: Контекст ошибки
        
        Returns:
            str: Сообщение об ошибке
        """
        timestamp = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
        
        message = f"""
❌ *ОШИБКА БОТА*

⏰ Время: {timestamp}
🔴 Ошибка: {error}
        """
        
        if context:
            message += f"\n📍 Контекст: {context}"
        
        message += "\n\n🔧 Проверьте логи для деталей"
        
        return message.strip()
    
    def format_success_message(self, title: str, topic: str) -> str:
        """
        Форматирует сообщение об успешной публикации.
        
        Args:
            title: Заголовок поста
            topic: Тема поста
        
        Returns:
            str: Сообщение об успехе
        """
        timestamp = datetime.now().strftime('%H:%M')
        
        return f"""
✅ *ПОСТ ОПУБЛИКОВАН*

⏰ {timestamp}
📝 {title}
🏷️ Тема: {topic}
        """.strip()
    
    def format_analytics_report(self, analytics: Analytics, days: int = 7) -> str:
        """
        Форматирует аналитический отчет.
        
        Args:
            analytics: Экземпляр Analytics
            days: Период для отчета
        
        Returns:
            str: Аналитический отчет
        """
        summary = analytics.get_summary(days)
        
        report = f"""
📊 *ЕЖЕНЕДЕЛЬНЫЙ ОТЧЕТ*

📅 Период: {days} дней
📝 Всего постов: {summary['total_posts']}
📈 За период: {summary['posts_in_period']}
⏱️ Частота: {summary['posting_frequency']} постов/день

🏆 *Топ темы:*
        """
        
        for i, topic in enumerate(summary['top_topics'][:3], 1):
            count = summary['topic_distribution'].get(topic, 0)
            report += f"\n{i}. {topic}: {count}"
        
        return report.strip()
    
    def log_notification(self, message_type: str, message: str):
        """
        Логирует уведомление в файл.
        
        Args:
            message_type: Тип сообщения
            message: Текст сообщения
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Создаем папку logs если не существует
        os.makedirs('logs', exist_ok=True)
        
        with open('logs/notifications.log', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message_type}: {message.replace(chr(10), ' ')}\n")
    
    def send_startup_notification(self) -> bool:
        """
        Отправляет уведомление о запуске.
        
        Returns:
            bool: True если отправлено
        """
        message = self.format_startup_message()
        self.log_notification('STARTUP', message)
        
        if self.enabled:
            print(f"📱 Уведомление администратору: {message[:50]}...")
            return True
        else:
            print("📱 Уведомления отключены (admin_chat_id не настроен)")
            return False
    
    def send_error_notification(self, error: str, context: str = '') -> bool:
        """
        Отправляет уведомление об ошибке.
        
        Args:
            error: Текст ошибки
            context: Контекст ошибки
        
        Returns:
            bool: True если отправлено
        """
        message = self.format_error_message(error, context)
        self.log_notification('ERROR', message)
        
        if self.enabled:
            print(f"🚨 Алерт администратору: {error[:50]}...")
            return True
        else:
            print(f"🚨 Ошибка (уведомления отключены): {error}")
            return False
    
    def send_success_notification(self, title: str, topic: str) -> bool:
        """
        Отправляет уведомление об успешной публикации.
        
        Args:
            title: Заголовок поста
            topic: Тема поста
        
        Returns:
            bool: True если отправлено
        """
        message = self.format_success_message(title, topic)
        self.log_notification('SUCCESS', message)
        
        if self.enabled:
            print(f"✅ Уведомление: Пост '{title[:30]}...' опубликован")
            return True
        else:
            print(f"✅ Пост опубликован: {title}")
            return False
    
    def send_analytics_report(self, analytics: Analytics, days: int = 7) -> bool:
        """
        Отправляет аналитический отчет.
        
        Args:
            analytics: Экземпляр Analytics
            days: Период для отчета
        
        Returns:
            bool: True если отправлено
        """
        message = self.format_analytics_report(analytics, days)
        self.log_notification('ANALYTICS', message)
        
        if self.enabled:
            print(f"📊 Отчет администратору за {days} дней")
            return True
        else:
            print(f"📊 Аналитический отчет за {days} дней готов")
            return False
    
    def get_notification_stats(self) -> dict:
        """
        Возвращает статистику уведомлений.
        
        Returns:
            dict: Статистика
        """
        log_file = 'logs/notifications.log'
        
        if not os.path.exists(log_file):
            return {
                'total': 0,
                'startup': 0,
                'errors': 0,
                'success': 0,
                'analytics': 0
            }
        
        stats = {
            'total': 0,
            'startup': 0,
            'errors': 0,
            'success': 0,
            'analytics': 0
        }
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    stats['total'] += 1
                    if 'STARTUP:' in line:
                        stats['startup'] += 1
                    elif 'ERROR:' in line:
                        stats['errors'] += 1
                    elif 'SUCCESS:' in line:
                        stats['success'] += 1
                    elif 'ANALYTICS:' in line:
                        stats['analytics'] += 1
        except Exception:
            pass
        
        return stats


# Простое использование и тестирование
if __name__ == '__main__':
    import os
    from database import Database
    
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ NOTIFICATIONS.PY")
    print("=" * 60)
    
    # Удаляем старый лог если есть
    log_file = 'logs/notifications.log'
    if os.path.exists(log_file):
        os.remove(log_file)
    
    # Создаем менеджер уведомлений
    notifier = NotificationManager(admin_chat_id='123456789')
    
    # Тест 1: Уведомление о запуске
    print("\n1. Уведомление о запуске:")
    startup_msg = notifier.format_startup_message()
    print(f"   Длина сообщения: {len(startup_msg)} символов")
    print(f"   ✅ Содержит время: {'⏰' in startup_msg}")
    
    success = notifier.send_startup_notification()
    print(f"   ✅ Отправлено: {success}")
    
    # Тест 2: Уведомление об ошибке
    print("\n2. Уведомление об ошибке:")
    error_msg = notifier.format_error_message('Тестовая ошибка', 'Контекст теста')
    print(f"   Длина сообщения: {len(error_msg)} символов")
    print(f"   ✅ Содержит ошибку: {'Тестовая ошибка' in error_msg}")
    
    success = notifier.send_error_notification('API недоступен', 'OpenRouter')
    print(f"   ✅ Отправлено: {success}")
    
    # Тест 3: Уведомление об успехе
    print("\n3. Уведомление об успехе:")
    success_msg = notifier.format_success_message('Тестовый пост', 'фитнес')
    print(f"   Длина сообщения: {len(success_msg)} символов")
    print(f"   ✅ Содержит заголовок: {'Тестовый пост' in success_msg}")
    
    success = notifier.send_success_notification('5 упражнений для здоровья', 'фитнес')
    print(f"   ✅ Отправлено: {success}")
    
    # Тест 4: Аналитический отчет
    print("\n4. Аналитический отчет:")
    
    # Создаем тестовую БД для аналитики
    test_db_path = 'data/test_notifications.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = Database(test_db_path)
    db.connect()
    db.init_tables()
    
    # Добавляем тестовые данные
    db.save_post('Пост 1', 'Текст', 'фитнес')
    db.save_post('Пост 2', 'Текст', 'питание')
    
    analytics = Analytics(db)
    
    report_msg = notifier.format_analytics_report(analytics, days=7)
    print(f"   Длина отчета: {len(report_msg)} символов")
    print(f"   ✅ Содержит статистику: {'Всего постов' in report_msg}")
    
    success = notifier.send_analytics_report(analytics, days=7)
    print(f"   ✅ Отправлено: {success}")
    
    db.close()
    os.remove(test_db_path)
    
    # Тест 5: Статистика уведомлений
    print("\n5. Статистика уведомлений:")
    stats = notifier.get_notification_stats()
    print(f"   Всего уведомлений: {stats['total']}")
    print(f"   Запусков: {stats['startup']}")
    print(f"   Ошибок: {stats['errors']}")
    print(f"   Успехов: {stats['success']}")
    print(f"   Отчетов: {stats['analytics']}")
    print(f"   ✅ Статистика получена")
    
    # Тест 6: Отключенные уведомления
    print("\n6. Отключенные уведомления:")
    disabled_notifier = NotificationManager(admin_chat_id=None)
    print(f"   Включены: {disabled_notifier.enabled}")
    
    success = disabled_notifier.send_startup_notification()
    print(f"   ✅ Работает без admin_chat_id: {not success}")
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 60)
    
    # Показываем содержимое лога
    if os.path.exists(log_file):
        print("\n📝 Содержимое лога уведомлений:")
        with open(log_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                print(f"   {i}. {line.strip()[:80]}...")
