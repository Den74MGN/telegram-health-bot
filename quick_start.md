# Быстрый Старт: Запуск за 15 Минут

## Минимальные Шаги для Запуска

### 1. Получите API Ключи (5 минут)

**Telegram Bot:**
- Напишите @BotFather: `/newbot`
- Сохраните токен бота

**OpenAI:**
- Зарегистрируйтесь на platform.openai.com
- Создайте API ключ в разделе "API Keys"

**Telega.in:**
- Зарегистрируйтесь на telega.in
- Получите API ключи после верификации

### 2. Создайте Канал (3 минуты)

1. В Telegram: Создать канал → Публичный канал
2. Добавьте бота как администратора
3. Сохраните @username канала

### 3. Установите Бота (5 минут)

**Windows:**
```bash
# Установите Python (python.org)
# Установите Git (git-scm.com)

# Клонируйте проект
git clone <repository_url>
cd telegram_health_bot

# Установите зависимости
pip install -r requirements.txt

# Создайте конфигурацию
cp .env.example .env
# Отредактируйте .env файл с вашими ключами
```

**Linux/Mac:**
```bash
sudo apt install python3-pip ffmpeg  # Ubuntu/Debian
pip3 install -r requirements.txt
```

### 4. Запустите Бота (2 минуты)

```bash
# Запуск
python main.py

# Ожидайте сообщения в консоли:
# "Бот запущен успешно"
# Через 2 часа - первый пост в канале
```

## Конфигурация (.env файл)

```env
TELEGRAM_BOT_TOKEN=ваш_бот_токен
TELEGRAM_CHANNEL_ID=@ваш_канал
TELEGRAM_ADMIN_CHAT_ID=ваш_user_id

OPENAI_API_KEY=sk-ваш_openai_ключ

TELEGIN_API_KEY=ваш_telegain_ключ
TELEGIN_API_SECRET=ваш_telegain_секрет

CONTENT_INTERVAL_HOURS=2
LOG_LEVEL=INFO
```

## Проверка Работы

1. **Логи:** `tail -f logs/bot.log`
2. **Посты:** Проверьте канал через 2 часа
3. **Ошибки:** Смотрите уведомления в админ чате

## Что Делать Если Не Работает

### Проблема: Нет постов в канале
```bash
# Проверьте подключение
python -c "
import asyncio
from module_publisher import TelegramPublisher

async def test():
    pub = TelegramPublisher('ВАШ_TOKEN', '@ВАШ_КАНАЛ')
    print('Подключение:', await pub.test_connection())

asyncio.run(test())
"
```

### Проблема: Ошибки генерации контента
```bash
# Тест OpenAI
python -c "
from module_content import ContentGenerator
gen = ContentGenerator('ВАШ_OPENAI_KEY')
print(gen.generate_text_post())
"
```

## Мониторинг

```bash
# Статус бота
docker ps | grep health-bot

# Логи в реальном времени
docker logs -f health-bot

# Остановка/запуск
docker stop health-bot
docker start health-bot
```

## Монетизация

- **Минимальный канал:** 1000 подписчиков
- **Доход:** 500-5000 RUB за пост
- **Выплаты:** Автоматически на карту/кошелек

## Поддержка

- Логи: `logs/bot.log` и `logs/error.log`
- Уведомления: Админ чат в Telegram
- Диагностика: Команды в разделе "Мониторинг"

**Готово!** Ваш бот теперь работает автономно и приносит доход.