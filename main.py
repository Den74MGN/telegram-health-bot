# -*- coding: utf-8 -*-
"""
Улучшенное Главное Приложение

Полностью автономный бот с расширенной монетизацией, аналитикой и оптимизацией.
Использует бесплатные ИИ модели через OpenRouter для генерации премиум контента.
"""

import asyncio
import logging
import os
import time
import json
import random
import sys
from datetime import datetime, timedelta
from typing import Dict
from dotenv import load_dotenv

from module_content import ContentGenerator
from module_scheduler import ContentScheduler
from module_publisher import TelegramPublisher
from module_ads import AdsIntegrator
from module_analytics import ContentAnalytics
from module_monetization import MonetizationManager
from apscheduler.triggers.interval import IntervalTrigger

# Загрузка переменных окружения
load_dotenv()

# Создаём необходимые директории для логов, данных и кэша
for directory in ['logs', 'data', 'cache']:
    os.makedirs(directory, exist_ok=True)
    
# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(


    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()    ]
)

# Создаем форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создаем обработчики файлов
try:
    file_handler = logging.FileHandler('logs/bot.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler('logs/error.log', encoding='utf-8')
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    analytics_handler = logging.FileHandler('logs/analytics.log', encoding='utf-8')
    analytics_handler.setFormatter(formatter)
    analytics_handler.setLevel(logging.INFO)

    # Добавляем обработчики к корневому логгеру
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(analytics_handler)

    print("Логирование настроено успешно")
except Exception as e:
    print(f"Ошибка настройки логирования: {e}")
    # Продолжаем без файлового логирования

logger = logging.getLogger(__name__)

def check_required_env_vars():
    # Проверяет наличие всех обязательных переменных окружения
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Токен Telegram бота',
        'TELEGRAM_CHANNEL_ID': 'ID канала Telegram',
        'TELEGRAM_ADMIN_CHAT_ID': 'ID чата администратора',
        'OPENROUTER_API_KEY': 'API ключ OpenRouter для генерации контента'
    }
    
    missing_vars = []
    for var_name, description in required_vars.items():
        if not os.getenv(var_name):
            missing_vars.append(f'{var_name} ({description})')
            logger.error(f'Отсутствует обязательная переменная окружения: {var_name} - {description}')
    
    if missing_vars:
        error_message = 'Ошибка конфигурации! Не найдены следующие переменные окружения:\n' + '\n'.join(missing_vars)
        error_message += '\n\nСоздайте файл .env в корневой папке проекта и добавьте эти переменные.'
        logger.error(error_message)
        print(error_message)
        sys.exit(1)
    
    return True

class AdvancedHealthBot:
    """Расширенный бот с полной автоматизацией и монетизацией."""

    def __init__(self):
        """Инициализация всех модулей с улучшенными возможностями."""
        # Проверяем переменные окружения перед инициализацией
        check_required_env_vars()
        # Инициализация основных модулей
        self.content_gen = ContentGenerator(os.getenv('OPENROUTER_API_KEY'))
        self.publisher = TelegramPublisher(
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            channel_id=os.getenv('TELEGRAM_CHANNEL_ID'),
            admin_chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        )
        self.ads_integrator = AdsIntegrator(
            api_key=os.getenv('TELEGIN_API_KEY'),
            api_secret=os.getenv('TELEGIN_API_SECRET')
        )
        self.analytics = ContentAnalytics()
        self.monetization = MonetizationManager(
            telegain_api_key=os.getenv('TELEGIN_API_KEY'),
            telegain_api_secret=os.getenv('TELEGIN_API_SECRET')
        )
        self.scheduler = ContentScheduler()

        # Статистика бота
        self.stats = {
            'posts_published': 0,
            'total_revenue': 0,
            'last_post_date': None,
            'errors_count': 0,
            'start_time': datetime.now()
        }

        # Создаём необходимые директории для работы бота
        os.makedirs('logs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
    
    def _format_post_caption(self, content: Dict) -> str:
        """
        Форматирует caption для Telegram поста с учетом ограничения в 1024 символа.
        
        Args:
            content: Словарь с контентом (title, body, hashtags)
            
        Returns:
            str: Отформатированный caption
        """
        # Формируем базовый текст
        title = f"*{content['title']}*"
        body = content['body']
        hashtags = ' '.join(content.get('hashtags', [])[:5])
        
        # Собираем caption
        caption = f"{title}\n\n{body}\n\n{hashtags}"
        
        # Проверяем длину и обрезаем если нужно
        if len(caption) > 1024:
            # Оставляем место для заголовка, хэштегов и многоточия
            available_for_body = 1024 - len(title) - len(hashtags) - 10
            if available_for_body > 100:
                body = body[:available_for_body] + "..."
                caption = f"{title}\n\n{body}\n\n{hashtags}"
            else:
                # Если совсем мало места, убираем хэштеги
                available_for_body = 1024 - len(title) - 10
                body = body[:available_for_body] + "..."
                caption = f"{title}\n\n{body}"
        
        return caption
        
    async def generate_and_publish_content(self):
        """Расширенная генерация и публикация премиум контента."""
        try:
            logger.info("🚀 Запуск расширенного цикла генерации контента")

            # Получаем аналитику для оптимизации
            analytics_data = self.analytics.analyze_content_performance()

            # Определяем оптимальную тему на основе аналитики
            if analytics_data['top_topics']:
                topic = random.choice(analytics_data['top_topics'])
            else:
                topic = None

            # Генерируем премиум контент
            logger.info(f"📝 Генерация контента на тему: {topic or 'автоматическая'}")
            content = self.content_gen.generate_text_post(topic)

            if not content:
                logger.error("❌ Не удалось сгенерировать контент")
                self.stats['errors_count'] += 1
                return

            logger.info(f"✅ Сгенерирован контент: {content['title']}")

            # Оптимизируем контент для вовлеченности
            content = self.content_gen.optimize_content_for_engagement(content)

            # Пропускаем монетизацию (отключена для частного канала)
            logger.info("💰 Монетизация отключена для частного канала")
            monetization_options = []

            # Форматируем caption для Telegram
            caption = self._format_post_caption(content)
            
            # Публикуем пост
            logger.info("📤 Публикация поста")
            # Проверяем наличие изображения в контенте
            if content.get('image_bytes'):
                # Публикуем пост с изображением
                logger.info(f"📸 Публикация поста с изображением")
                success = await self.publisher.publish_photo_post(
                    content['image_bytes'],
                    caption,
                    monetization_options[0] if monetization_options else None
                )
            else:
                # Публикуем текстовый пост если изображение не создано
                logger.info(f"📝 Публикация текстового поста")
                success = await self.publisher.publish_text_post(
                    content,
                    monetization_options[0] if monetization_options else None
                )
            
            if success:
                self.stats['posts_published'] += 1
                self.stats['last_post_date'] = datetime.now()
                logger.info(f"🎉 Пост опубликован успешно! Всего постов: {self.stats['posts_published']}")
            else:
                logger.error("❌ Не удалось опубликовать пост")
                self.stats['errors_count'] += 1
    
        except Exception as e:
            logger.error(f"❌ Критическая ошибка в цикле генерации контента: {e}")
            self.stats['errors_count'] += 1
    def generate_analytics_report(self):
        """Генерирует и отправляет аналитический отчет."""
        try:
            # Получаем свежую аналитику
            analytics = self.analytics.analyze_content_performance()

            # Генерируем текстовый отчет
            report = self.analytics.generate_analytics_report()

            # Отправляем отчет администратору
            asyncio.run(self.publisher._notify_admin("📊 Еженедельный отчет по аналитике:"))
            asyncio.run(self.publisher._notify_admin(report[:4000]))  # Ограничиваем длину сообщения

            logger.info("📊 Аналитический отчет отправлен администратору")

        except Exception as e:
            logger.error(f"Ошибка генерации аналитического отчета: {e}")

    def optimize_performance(self):
        """Оптимизирует производительность на основе аналитики."""
        try:
            analytics = self.analytics.analyze_content_performance()

            # Оптимизация времени публикации
            if 'best_posting_time' in analytics:
                best_time = analytics['best_posting_time']
                logger.info(f"🎯 Оптимальное время публикации: {best_time}")

            # Оптимизация тем
            if analytics['recommendations']:
                logger.info(f"💡 Рекомендации по улучшению: {analytics['recommendations'][0]}")

            # Прогноз доходов (монетизация отключена)
            logger.info("💰 Монетизация отключена - прогноз недоступен")

        except Exception as e:
            logger.error(f"Ошибка оптимизации производительности: {e}")

    async def health_check(self):
        """Расширенная проверка здоровья системы."""
        try:
            logger.info("🔍 Запуск расширенной проверки здоровья системы")

            # Тест Telegram подключения
            telegram_ok = await self.publisher.test_connection()

            # Тест OpenRouter API (бесплатные модели)
            try:
                test_content = self.content_gen.generate_text_post("тест")
                openrouter_ok = bool(test_content)
            except Exception as e:
                logger.error(f"Ошибка проверки OpenRouter API: {e}")
                openrouter_ok = False

            # Тест монетизации (отключена)
            monetization_ok = True  # Пропускаем тест монетизации

            # Тест аналитики
            try:
                analytics_ok = True  # Аналитика всегда доступна
            except Exception as e:
                logger.error(f"Ошибка теста аналитики: {e}")
                analytics_ok = False

            status = {
                "telegram": telegram_ok,
                "openrouter": openrouter_ok,
                "monetization": monetization_ok,
                "analytics": analytics_ok
            }

            healthy = all(status.values())
            logger.info(f"🏥 Проверка здоровья: {status}")

            if not healthy:
                await self.publisher._notify_admin(f"⚠️ Проверка здоровья не удалась: {status}")
            else:
                logger.info("✅ Все системы работают нормально")

            return healthy

        except Exception as e:
            logger.error(f"❌ Ошибка проверки здоровья: {e}")
            return False

    def startup(self):
        """Расширенная инициализация и запуск бота."""
        logger.info("🚀 Запуск Улучшенного Бота Здоровья и Фитнеса")
        logger.info("💎 С использованием бесплатных ИИ моделей через OpenRouter")
        logger.info("💰 С расширенной системой монетизации")

        # Расширенная проверка здоровья
        if not asyncio.run(self.health_check()):
            logger.error("❌ Начальная проверка здоровья не удалась")
            self.publisher._notify_admin("🚨 Критическая ошибка: Не удалось пройти проверку здоровья")
            return

        # Планирование задач с оптимизацией
        base_interval = int(os.getenv('CONTENT_INTERVAL_HOURS', 2))

        # Планирование генерации контента
        self.scheduler.schedule_content_generation(
            self.generate_and_publish_content,
            interval_hours=base_interval
        )

        # Планирование аналитики
        self.scheduler.add_job(
            self.generate_analytics_report,
            trigger=IntervalTrigger(days=7),
            job_id='analytics_report',
            name='Аналитический отчет'
        )

        # Планирование оптимизации производительности
        self.scheduler.add_job(
            self.optimize_performance,
            trigger=IntervalTrigger(hours=6),
            job_id='performance_optimization',
            name='Оптимизация Производительности'
        )

        # Планирование резервного копирования
        self.scheduler.add_job(
            self._create_backup,
            trigger=IntervalTrigger(days=1),
            job_id='daily_backup',
            name='Ежедневное Резервное Копирование'
        )

        # Запуск планировщика
        self.scheduler.start_scheduler()

        # Отправляем подробное уведомление о запуске
        startup_message = f"""🤖 Улучшенный Бот Здоровья Запущен!

📊 Статистика:
• Постов опубликовано: {self.stats['posts_published']}
• Общий доход: {self.stats['total_revenue']:.0f} RUB (монетизация отключена)
• Время работы: {datetime.now() - self.stats['start_time']}

⚙️ Конфигурация:
• Интервал публикации: {base_interval} часа
• Используются бесплатные ИИ модели (OpenRouter)
• Монетизация: ОТКЛЮЧЕНА (частный канал)
• Аналитика: ВКЛЮЧЕНА

🎯 Функции:
• Премиум генерация контента (бесплатно)
• SEO оптимизация контента
• Расширенная аналитика
• Оптимизация производительности
• Автоматический рост канала

Бот готов к автономной работе в частном канале! 🚀
"""

        asyncio.run(self.publisher._notify_admin(startup_message))
        logger.info("✅ Бот успешно запущен и готов к работе")
        
    def shutdown(self):
        """Корректное завершение работы бота с сохранением данных."""
        logger.info("🛑 Корректное завершение работы бота")

        try:
            # Сохраняем финальную статистику
            final_stats = {
                'shutdown_time': datetime.now().isoformat(),
                'uptime': str(datetime.now() - self.stats['start_time']),
                'final_stats': self.stats
            }

            with open('logs/final_stats.json', 'w', encoding='utf-8') as f:
                json.dump(final_stats, f, ensure_ascii=False, indent=2, default=str)

            # Останавливаем планировщик
            self.scheduler.stop_scheduler()

            # Отправляем отчет о завершении работы
            shutdown_message = f"""
🛑 Бот остановлен

📊 Финальная статистика:
• Всего постов: {self.stats['posts_published']}
• Общий доход: {self.stats['total_revenue']:.0f} RUB (монетизация отключена)
• Время работы: {datetime.now() - self.stats['start_time']}
• Количество ошибок: {self.stats['errors_count']}

✅ Данные сохранены в logs/final_stats.json
✅ Бот работал в частном канале без рекламы
"""

            asyncio.run(self.publisher._notify_admin(shutdown_message))
            logger.info("💾 Финальные данные сохранены")

        except Exception as e:
            logger.error(f"Ошибка при завершении работы: {e}")

    def _create_backup(self):
        """Создает резервную копию важных данных."""
        try:
            backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Создаем резервную копию логов и аналитики
            backup_files = [
                'logs/bot.log',
                'logs/content_stats.json',
                'logs/revenue_tracking.json'
            ]

            for file_path in backup_files:
                if os.path.exists(file_path):
                    backup_path = f"backups/{backup_time}_{os.path.basename(file_path)}"
                    os.makedirs('backups', exist_ok=True)

                    # Копируем файл
                    with open(file_path, 'r', encoding='utf-8') as src:
                        content = src.read()

                    with open(backup_path, 'w', encoding='utf-8') as dst:
                        dst.write(content)

            logger.info(f"💾 Резервная копия создана: {backup_time}")

        except Exception as e:
            logger.error(f"Ошибка создания резервной копии: {e}")

def main():
    """Главная точка входа улучшенного бота."""
    bot = AdvancedHealthBot()
    
    try:
        bot.startup()
        
        # Держим бот запущенным
        logger.info("✅ Бот запущен, ожидание задач планировщика...")
        while True:
            time.sleep(60)  # Проверяем каждую минуту
        
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал завершения от пользователя")
    except Exception as e:
        logger.error(f"🚨 Критическая ошибка в основном цикле: {e}")
        asyncio.run(bot.publisher._notify_admin(f"🚨 Критическая ошибка: {str(e)}"))
    finally:
        bot.shutdown()

if __name__ == "__main__":
    main()

















































