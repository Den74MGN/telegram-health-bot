# Инструкции по Настройке

## Предварительные Требования

- Python 3.8 или выше
- Docker (опционально, для контейнеризованного развертывания)
- Аккаунт Telegram
- Аккаунт OpenAI (доступен бесплатный тариф)
- Аккаунт на платформе Telega.in

## 1. Настройка Telegram Бота

### Создание Telegram Бота

1. Откройте Telegram и найдите `@BotFather`
2. Отправьте команду `/newbot`
3. Следуйте подсказкам для:
   - Выбора имени бота (например, "Бот Здоровья и Фитнеса")
   - Выбора username (например, "health_fitness_daily_bot")
4. Сохраните **Bot Token**, предоставленный BotFather

### Создание Telegram Канала

1. В Telegram создайте новый канал
2. Установите имя канала и описание
3. Добавьте вашего бота как администратора с правами публикации
4. Получите ID канала:
   - Для публичных каналов: `@channelusername`
   - Для приватных каналов: Используйте бота вроде `@userinfobot` или проверьте логи бота

### Опционально: Админ Чат для Уведомлений

1. Создайте приватный чат с вашим ботом
2. Отправьте сообщение, чтобы получить chat ID
3. Используйте `@userinfobot`, чтобы получить ваш user ID для уведомлений администратора

## 2. Настройка OpenAI API

1. Перейдите на [OpenAI Platform](https://platform.openai.com/)
2. Зарегистрируйтесь или войдите в систему
3. Перейдите в раздел API Keys
4. Создайте новый API ключ
5. Сохраните API ключ в безопасном месте

**Примечание:** Используйте модель GPT-3.5-turbo, которая имеет бесплатный тариф.

## 3. Настройка Платформы Telega.in

1. Зарегистрируйтесь на [Telega.in](https://telega.in/)
2. Завершите верификацию аккаунта
3. Получите API учетные данные:
   - API Key
   - API Secret
4. Настройте способ оплаты для получения дохода от рекламы

## 4. Конфигурация Окружения

Создайте файл `.env` в корне проекта:

```env
# Конфигурация Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username
TELEGRAM_ADMIN_CHAT_ID=your_admin_chat_id

# Конфигурация OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Конфигурация Telega.in
TELEGIN_API_KEY=your_telegain_api_key_here
TELEGIN_API_SECRET=your_telegain_api_secret_here

# Настройки Приложения
CONTENT_INTERVAL_HOURS=2
LOG_LEVEL=INFO
```

## 5. Установка

### Вариант A: Локальная Установка

1. Склонируйте или скачайте файлы проекта
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Скопируйте файл `.env` в директорию проекта

### Вариант B: Установка через Docker

1. Соберите Docker образ:
   ```bash
   docker build -t telegram-health-bot .
   ```
2. Запустите контейнер:
   ```bash
   docker run -d --env-file .env --name health-bot telegram-health-bot
   ```

## 6. Тестирование Настройки

### Тест Подключения к Telegram

Запустите быстрый тест для проверки подключения бота:

```python
from module_publisher import TelegramPublisher
import asyncio

async def test():
    publisher = TelegramPublisher(
        bot_token="your_bot_token",
        channel_id="@your_channel"
    )
    success = await publisher.test_connection()
    print(f"Тест подключения: {'УСПЕХ' if success else 'НЕУДАЧА'}")

asyncio.run(test())
```

### Тест Генерации Контента

```python
from module_content import ContentGenerator

generator = ContentGenerator(openai_api_key="your_openai_key")
content = generator.generate_text_post("fitness tips")
print(content)
```

### Тест Интеграции Рекламы

```python
from module_ads import AdsIntegrator

ads = AdsIntegrator(
    api_key="your_telegain_key",
    api_secret="your_telegain_secret"
)
ad = ads.get_advertisement()
print(ad)
```

## 7. Запуск Приложения

### Локальный Запуск

```bash
python main.py
```

### Запуск через Docker

```bash
docker run -d --env-file .env telegram-health-bot
```

### Мониторинг Логов

```bash
# Локально
tail -f logs/bot.log

# Docker
docker logs -f health-bot
```

## 8. Устранение Неисправностей

### Распространенные Проблемы

1. **Бот не публикует в канал**
   - Убедитесь, что бот добавлен как администратор
   - Проверьте формат ID канала
   - Убедитесь, что токен бота корректен

2. **Ошибки OpenAI API**
   - Проверьте валидность API ключа
   - Убедитесь, что на аккаунте есть кредиты
   - Проверьте ограничения скорости

3. **Реклама не загружается**
   - Проверьте учетные данные Telega.in
   - Проверьте доступность API эндпоинтов
   - Подтвердите верификацию аккаунта

4. **Генерация видео не работает**
   - Установите ffmpeg: `apt-get install ffmpeg`
   - Проверьте доступное дисковое пространство
   - Проверьте зависимости MoviePy

### Анализ Логов

Проверяйте логи на паттерны ошибок:
- `ERROR` - Критические сбои
- `WARNING` - Потенциальные проблемы
- `INFO` - Нормальная работа

### Проверки Здоровья

Приложение включает встроенный мониторинг здоровья. Проверяйте админ чат на системные уведомления.

## 9. Продакшн Развертывание

### Развертывание на VPS

1. Выберите провайдера VPS (DigitalOcean, Vultr, etc.)
2. Установите Docker
3. Загрузите файлы проекта
4. Настройте systemd для авто-перезапуска:
   ```bash
   sudo nano /etc/systemd/system/health-bot.service
   ```

   ```ini
   [Unit]
   Description=Telegram Health Bot
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/path/to/project
   ExecStart=/usr/bin/docker run --env-file .env telegram-health-bot
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. Включите и запустите сервис:
   ```bash
   sudo systemctl enable health-bot
   sudo systemctl start health-bot
   ```

### Мониторинг

- Настройте ротацию логов
- Настройте мониторинг сервера (опционально)
- Регулярное резервное копирование логов и конфигурации

## 10. Лучшие Практики Безопасности

- Храните API ключи безопасно (переменные окружения, не в коде)
- Используйте HTTPS для API коммуникаций
- Регулярно обновляйте API ключи
- Мониторьте необычную активность
- Поддерживайте зависимости в актуальном состоянии