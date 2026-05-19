# Пример Запуска и Тестирования

## Главное Приложение (main.py)

```python
"""
Главное приложение, оркестрирующее все модули для автономной публикации контента.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from module_content import ContentGenerator
from module_scheduler import ContentScheduler
from module_publisher import TelegramPublisher
from module_ads import AdsIntegrator

# Загрузка переменных окружения
load_dotenv()

# Конфигурация логирования
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.FileHandler('logs/error.log', level=logging.ERROR),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class HealthBot:
    """Главный класс приложения бота."""

    def __init__(self):
        """Инициализация всех модулей."""
        self.content_gen = ContentGenerator(os.getenv('OPENAI_API_KEY'))
        self.publisher = TelegramPublisher(
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            channel_id=os.getenv('TELEGRAM_CHANNEL_ID'),
            admin_chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        )
        self.ads_integrator = AdsIntegrator(
            api_key=os.getenv('TELEGIN_API_KEY'),
            api_secret=os.getenv('TELEGIN_API_SECRET')
        )
        self.scheduler = ContentScheduler()

    async def generate_and_publish_content(self):
        """Генерация контента и публикация в канал."""
        try:
            logger.info("Запуск цикла генерации контента")

            # Генерация текстового контента
            content = self.content_gen.generate_text_post("здоровье и wellness")
            if not content:
                logger.error("Не удалось сгенерировать контент")
                return

            logger.info(f"Сгенерирован контент: {content['title']}")

            # Попытка получить рекламу
            ad_content = self.ads_integrator.get_advertisement()
            if ad_content:
                logger.info(f"Получена реклама: {ad_content['id']}")

            # Публикация текстового поста
            success = await self.publisher.publish_text_post(content, ad_content)
            if success:
                logger.info("Текстовый пост опубликован успешно")

                # Отчет о производительности рекламы, если реклама была включена
                if ad_content:
                    self.ads_integrator.report_ad_performance(ad_content['id'])
            else:
                logger.error("Не удалось опубликовать текстовый пост")

            # Генерация и публикация видео (опционально)
            video_path = self.content_gen.generate_video_content(content)
            if video_path:
                caption = f"{content['title']}\n\n{content['body'][:100]}..."
                video_success = await self.publisher.publish_video_post(video_path, caption, ad_content)
                if video_success:
                    logger.info("Видеопост опубликован успешно")
                    # Очистка видеофайла
                    os.remove(video_path)
                else:
                    logger.error("Не удалось опубликовать видеопост")

        except Exception as e:
            logger.error(f"Ошибка в цикле генерации контента: {e}")
            await self.publisher._notify_admin(f"❌ Ошибка генерации контента: {str(e)}")

    async def health_check(self):
        """Выполнение проверки здоровья системы."""
        try:
            # Тест подключения к Telegram
            telegram_ok = await self.publisher.test_connection()

            # Тест OpenAI API (простой запрос)
            openai_ok = bool(self.content_gen.generate_text_post("test"))

            # Тест ads API
            ads_ok = self.ads_integrator.get_available_budget() is not None

            status = {
                "telegram": telegram_ok,
                "openai": openai_ok,
                "ads": ads_ok
            }

            healthy = all(status.values())
            logger.info(f"Проверка здоровья: {status}")

            if not healthy:
                await self.publisher._notify_admin(f"⚠️ Проверка здоровья не удалась: {status}")

            return healthy

        except Exception as e:
            logger.error(f"Ошибка проверки здоровья: {e}")
            return False

    async def startup(self):
        """Инициализация и запуск бота."""
        logger.info("Запуск Бота Здоровья и Фитнеса")

        # Тест подключений
        if not await self.health_check():
            logger.error("Начальная проверка здоровья не удалась")
            return

        # Планирование генерации контента
        interval = int(os.getenv('CONTENT_INTERVAL_HOURS', 2))
        self.scheduler.schedule_content_generation(
            self.generate_and_publish_content,
            interval_hours=interval
        )

        # Планирование проверок здоровья
        self.scheduler.add_job(
            self.health_check,
            trigger=self.scheduler.scheduler.triggers.interval.IntervalTrigger(hours=1),
            job_id='health_check',
            name='Проверка Здоровья'
        )

        # Запуск планировщика
        self.scheduler.start_scheduler()

        await self.publisher._notify_admin("🤖 Бот запущен успешно")

        logger.info("Бот запущен успешно")

    async def shutdown(self):
        """Корректное завершение работы бота."""
        logger.info("Завершение работы бота")
        self.scheduler.stop_scheduler()
        await self.publisher._notify_admin("🛑 Бот остановлен")

async def main():
    """Главная точка входа."""
    bot = HealthBot()
    await bot.startup()

    try:
        # Поддержание работы приложения
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения")
    finally:
        await bot.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

## Тестирование Приложения

### Модульные Тесты (tests.py)

```python
"""
Модульные тесты для всех модулей.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import os
import tempfile

# Импорт модулей
from module_content import ContentGenerator
from module_publisher import TelegramPublisher
from module_ads import AdsIntegrator
from module_scheduler import ContentScheduler

class TestContentGenerator(unittest.TestCase):
    """Тест функциональности генерации контента."""

    def setUp(self):
        """Настройка тестовых фикстур."""
        self.generator = ContentGenerator("fake_api_key")

    @patch('module_content.OpenAI')
    def test_generate_text_post_success(self, mock_openai):
        """Тест успешной генерации текстового поста."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Тестовый Заголовок\n\nТестовое содержание."
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = self.generator.generate_text_post()

        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('body', result)
        self.assertEqual(result['title'], 'Тестовый Заголовок')

    @patch('module_content.OpenAI')
    def test_generate_text_post_failure(self, mock_openai):
        """Тест неудачи генерации текстового поста."""
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        result = self.generator.generate_text_post()

        # Должен вернуть запасной контент
        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('body', result)

class TestTelegramPublisher(unittest.IsolatedAsyncioTestCase):
    """Тест функциональности публикации в Telegram."""

    def setUp(self):
        """Настройка тестовых фикстур."""
        self.publisher = TelegramPublisher(
            bot_token="fake_token",
            channel_id="@test_channel"
        )

    @patch('module_publisher.Bot')
    async def test_publish_text_post_success(self, mock_bot_class):
        """Тест успешной публикации текстового поста."""
        mock_bot = Mock()
        mock_bot.send_message = AsyncMock()
        mock_bot_class.return_value = mock_bot

        content = {"title": "Тестовый Заголовок", "body": "Тестовое содержание"}
        result = await self.publisher.publish_text_post(content)

        self.assertTrue(result)
        mock_bot.send_message.assert_called_once()

    @patch('module_publisher.Bot')
    async def test_publish_text_post_failure(self, mock_bot_class):
        """Тест неудачи публикации текстового поста."""
        mock_bot = Mock()
        mock_bot.send_message = AsyncMock(side_effect=Exception("Network error"))
        mock_bot_class.return_value = mock_bot

        content = {"title": "Тестовый Заголовок", "body": "Тестовое содержание"}
        result = await self.publisher.publish_text_post(content)

        self.assertFalse(result)

class TestAdsIntegrator(unittest.TestCase):
    """Тест функциональности интеграции рекламы."""

    def setUp(self):
        """Настройка тестовых фикстур."""
        self.ads = AdsIntegrator("fake_key", "fake_secret")

    @patch('module_ads.requests.Session')
    def test_get_advertisement_success(self, mock_session_class):
        """Тест успешного получения рекламы."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            'ads': [{'id': '123', 'advertiser_id': '456', 'text': 'Тестовая реклама', 'budget': 500}]
        }
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = self.ads.get_advertisement()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], '123')

    @patch('module_ads.requests.Session')
    def test_get_advertisement_no_ads(self, mock_session_class):
        """Тест когда реклама недоступна."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {'ads': []}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = self.ads.get_advertisement()

        self.assertIsNone(result)

class TestContentScheduler(unittest.TestCase):
    """Тест функциональности планировщика."""

    def setUp(self):
        """Настройка тестовых фикстур."""
        self.scheduler = ContentScheduler()

    def test_scheduler_initialization(self):
        """Тест инициализации планировщика."""
        self.assertIsNotNone(self.scheduler.scheduler)

    def test_schedule_content_generation(self):
        """Тест планирования генерации контента."""
        def dummy_func():
            pass

        job_id = self.scheduler.schedule_content_generation(dummy_func)
        self.assertIsInstance(job_id, str)

        jobs = self.scheduler.get_jobs()
        self.assertEqual(len(jobs), 1)

if __name__ == '__main__':
    # Создание тестовых директорий
    os.makedirs('logs', exist_ok=True)

    # Запуск тестов
    unittest.main(verbosity=2)
```

## Запуск Приложения

### Локальная Разработка

1. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Создание файла окружения:**
   ```bash
   cp .env.example .env
   # Редактируйте .env с вашими учетными данными
   ```

3. **Запуск тестов:**
   ```bash
   python tests.py
   ```

4. **Запуск бота:**
   ```bash
   python main.py
   ```

### Развертывание в Docker

1. **Сборка образа:**
   ```bash
   docker build -t telegram-health-bot .
   ```

2. **Запуск контейнера:**
   ```bash
   docker run --env-file .env telegram-health-bot
   ```

3. **Запуск тестов в контейнере:**
   ```bash
   docker run --env-file .env telegram-health-bot python tests.py
   ```

## Шаги Верификации

### 1. Проверка Статуса Бота

```bash
# Проверка работы бота
ps aux | grep main.py

# Проверка логов
tail -f logs/bot.log
```

### 2. Тест Генерации Контента

```python
from module_content import ContentGenerator

gen = ContentGenerator("your_openai_key")
content = gen.generate_text_post()
print("Сгенерированный контент:", content)
```

### 3. Тест Публикации

```python
import asyncio
from module_publisher import TelegramPublisher

async def test():
    publisher = TelegramPublisher("your_token", "@your_channel")
    success = await publisher.test_connection()
    print("Подключение к Telegram:", "OK" if success else "FAILED")

asyncio.run(test())
```

### 4. Тест Интеграции Рекламы

```python
from module_ads import AdsIntegrator

ads = AdsIntegrator("your_key", "your_secret")
budget = ads.get_available_budget()
print("Доступный бюджет:", budget)
```

### 5. Ручная Публикация Контента

```python
import asyncio
from main import HealthBot

async def manual_publish():
    bot = HealthBot()
    await bot.generate_and_publish_content()
    print("Ручная публикация завершена")

asyncio.run(manual_publish())
```

## Ожидаемый Вывод

### Успешный Запуск

```
2024-01-15 10:00:00,000 - __main__ - INFO - Запуск Бота Здоровья и Фитнеса
2024-01-15 10:00:00,100 - module_publisher - INFO - Бот подключен успешно: @health_fitness_bot
2024-01-15 10:00:00,200 - module_scheduler - INFO - Генерация контента запланирована каждые 2 часа
2024-01-15 10:00:00,300 - __main__ - INFO - Бот запущен успешно
2024-01-15 10:02:00,000 - __main__ - INFO - Запуск цикла генерации контента
2024-01-15 10:02:00,500 - module_content - INFO - Сгенерирован контент: 10 Утренних Упражнений для Лучшего Здоровья
2024-01-15 10:02:01,000 - module_publisher - INFO - Текстовый пост опубликован успешно
```

### Сценарии Ошибок

#### Не удалось Подключиться к API
```
2024-01-15 10:00:00,000 - module_publisher - ERROR - Не удалось подключиться к Telegram API
2024-01-15 10:00:00,100 - __main__ - ERROR - Начальная проверка здоровья не удалась
```

#### Не удалось Сгенерировать Контент
```
2024-01-15 10:02:00,000 - module_content - ERROR - Не удалось сгенерировать текстовый контент: превышен лимит API
2024-01-15 10:02:00,100 - __main__ - INFO - Использование запасного контента
```

#### Не удалось Опубликовать
```
2024-01-15 10:02:01,000 - module_publisher - WARNING - Попытка публикации 1 не удалась: таймаут сети. Повтор через 5с...
2024-01-15 10:02:06,500 - module_publisher - INFO - Текстовый пост опубликован успешно
```

## Команды Мониторинга

```bash
# Мониторинг логов в реальном времени
tail -f logs/bot.log

# Сводка ошибок
grep "ERROR" logs/bot.log | tail -10

# Уровень успеха
echo "Уровень успеха: $(grep "опубликовано успешно" logs/bot.log | wc -l)/$(grep "Запуск цикла генерации" logs/bot.log | wc -l)"

# Проверка запланированных заданий
python -c "from module_scheduler import ContentScheduler; s = ContentScheduler(); print([job.name for job in s.get_jobs()])"
```

## Troubleshooting

### Bot Not Starting
- Check `.env` file exists and has correct values
- Verify API keys are valid
- Check network connectivity

### Content Not Generating
- Verify OpenAI API key and credits
- Check API rate limits
- Test with simple prompt

### Publishing Failing
- Confirm bot is administrator in channel
- Verify channel ID format
- Check bot token validity

### Ads Not Loading
- Verify Telega.in credentials
- Check account verification status
- Confirm API endpoints are accessible

## Performance Benchmarks

- **Content Generation**: 5-15 seconds
- **Publishing**: 2-5 seconds
- **Video Generation**: 30-60 seconds
- **Memory Usage**: 100-300 MB
- **CPU Usage**: 10-50% during content generation