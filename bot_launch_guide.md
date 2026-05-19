# Подробное Руководство по Запуску Telegram Бота Здоровья

## Что Вам Нужно Перед Запуском

### Обязательные Аккаунты и Сервисы

1. **Telegram Аккаунт**
   - Создайте аккаунт в Telegram (если у вас его нет)
   - Номер телефона для регистрации

2. **OpenAI Аккаунт**
   - Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com/)
   - Получите бесплатный API ключ (бесплатный тариф доступен)
   - Бесплатный лимит: около $5-10 в месяц на старте

3. **Telega.in Аккаунт**
   - Зарегистрируйтесь на [telega.in](https://telega.in/)
   - Пройдите верификацию аккаунта
   - Получите API ключи для монетизации

4. **Компьютер/Сервер**
   - Python 3.8 или выше
   - Минимум 2GB RAM
   - Стабильное интернет-соединение
   - Опционально: VPS сервер для постоянной работы

## Шаг 1: Создание Telegram Бота

### 1.1 Создание Бота через BotFather

1. Откройте Telegram
2. Найдите бота `@BotFather`
3. Отправьте команду: `/newbot`
4. Придумайте имя бота (например: "Здоровье и Фитнес Бот")
5. Придумайте username бота (должен заканчиваться на _bot)
6. Сохраните **Bot Token** - это ваш ключ для API

**Пример вывода от BotFather:**
```
Done! Congratulations on your new bot. You will find it at t.me/YourBotName. You can now add a description, about section and profile picture.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 1.2 Создание Канала для Публикаций

1. В Telegram нажмите "Создать канал"
2. Выберите тип: "Канал"
3. Придумайте название (например: "Здоровье и Фитнес")
4. Создайте публичный адрес (username канала)
5. Добавьте бота как администратора:
   - Зайдите в канал
   - Нажмите "Управление каналом"
   - "Администраторы" → "Добавить администратора"
   - Найдите вашего бота и добавьте его

### 1.3 Получение ID Канала

**Для публичных каналов:**
- ID = @username_канала (например: @health_fitness)

**Для приватных каналов:**
- Используйте бота @userinfobot:
  - Отправьте боту сообщение с ссылкой на канал
  - Получите chat ID в формате -1001234567890

## Шаг 2: Получение API Ключей

### 2.1 OpenAI API Ключ

1. Зайдите на [platform.openai.com](https://platform.openai.com/)
2. Войдите в аккаунт или зарегистрируйтесь
3. Перейдите в раздел "API Keys"
4. Нажмите "Create new secret key"
5. Скопируйте сгенерированный ключ
6. **Важно:** Ключ показывается только один раз!

### 2.2 Telega.in API Ключи

1. Зарегистрируйтесь на [telega.in](https://telega.in/)
2. Пройдите верификацию (может потребоваться фото документов)
3. В личном кабинете найдите раздел "API" или "Интеграция"
4. Сгенерируйте API Key и API Secret
5. Настройте способ вывода денег (карта, кошелек)

## Шаг 3: Установка и Настройка Бота

### Вариант A: Локальная Установка

#### 3.1 Установка Python

Если Python не установлен:

**Windows:**
```bash
# Скачайте с python.org
# Установите, отметив "Add to PATH"
python --version  # Проверьте версию
```

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install python3.8 python3-pip
python3 --version
```

#### 3.2 Установка Зависимостей

```bash
# Перейдите в папку проекта
cd telegram_health_bot

# Установите зависимости
pip install -r requirements.txt

# Проверьте установку
python -c "import telegram, openai, apscheduler; print('Все зависимости установлены')"
```

#### 3.3 Создание Файла Конфигурации

```bash
# Скопируйте шаблон
cp .env.example .env

# Откройте .env в редакторе
notepad .env  # Windows
nano .env     # Linux
```

**Заполните .env файл:**
```env
# Конфигурация Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID=@your_channel_username
TELEGRAM_ADMIN_CHAT_ID=your_user_id

# Конфигурация OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Конфигурация Telega.in
TELEGIN_API_KEY=your_telegain_api_key
TELEGIN_API_SECRET=your_telegain_api_secret

# Настройки Приложения
CONTENT_INTERVAL_HOURS=2
LOG_LEVEL=INFO
```

### Вариант B: Docker Установка (Рекомендуется)

#### 3.4 Установка Docker

**Windows:**
```bash
# Скачайте Docker Desktop с docker.com
# Установите и запустите
```

**Linux:**
```bash
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

#### 3.5 Сборка и Запуск Контейнера

```bash
# Сборка образа
docker build -t telegram-health-bot .

# Запуск контейнера
docker run -d --env-file .env --name health-bot telegram-health-bot

# Проверка статуса
docker ps | grep health-bot

# Просмотр логов
docker logs -f health-bot
```

## Шаг 4: Тестирование Бота

### 4.1 Тест Подключений

```python
# Создайте тестовый файл test_bot.py
from module_publisher import TelegramPublisher
import asyncio

async def test():
    publisher = TelegramPublisher(
        bot_token="ВАШ_BOT_TOKEN",
        channel_id="ВАШ_CHANNEL_ID"
    )
    success = await publisher.test_connection()
    print(f"Подключение к Telegram: {'УСПЕХ' if success else 'НЕУДАЧА'}")

asyncio.run(test())
```

Запустите тест:
```bash
python test_bot.py
```

### 4.2 Тест Генерации Контента

```python
# Тест генерации контента
from module_content import ContentGenerator

generator = ContentGenerator("ВАШ_OPENAI_API_KEY")
content = generator.generate_text_post("здоровье и фитнес")
print("Сгенерированный контент:")
print(f"Заголовок: {content['title']}")
print(f"Текст: {content['body']}")
```

### 4.3 Тест Рекламы

```python
# Тест интеграции рекламы
from module_ads import AdsIntegrator

ads = AdsIntegrator("ВАШ_TELEGAIN_KEY", "ВАШ_TELEGAIN_SECRET")
budget = ads.get_available_budget()
print(f"Доступный бюджет: {budget} RUB")

ad = ads.get_advertisement()
if ad:
    print(f"Получена реклама: {ad['text']}")
else:
    print("Реклама недоступна")
```

## Шаг 5: Первый Запуск Бота

### 5.1 Запуск в Режиме Разработки

```bash
# Локальный запуск
python main.py

# Ожидаемый вывод:
# 2024-01-15 10:00:00,000 - Запуск Бота Здоровья и Фитнеса
# 2024-01-15 10:00:00,100 - Бот подключен успешно: @your_bot
# 2024-01-15 10:00:00,200 - Генерация контента запланирована каждые 2 часа
# 2024-01-15 10:00:00,300 - Бот запущен успешно
```

### 5.2 Проверка Работы

1. **Проверьте логи:**
   ```bash
   tail -f logs/bot.log
   ```

2. **Проверьте канал в Telegram:**
   - Через 2 часа должен появиться первый пост
   - Пост должен содержать заголовок и текст о здоровье
   - Может включать рекламу (если доступна)

3. **Проверьте уведомления администратора:**
   - Бот должен отправить сообщение о успешном запуске
   - В ваш личный чат с ботом

## Шаг 6: Мониторинг и Поддержка

### 6.1 Мониторинг Работы

```bash
# Просмотр логов в реальном времени
tail -f logs/bot.log

# Проверка ошибок
grep "ERROR" logs/bot.log

# Проверка успешных публикаций
grep "опубликовано успешно" logs/bot.log

# Проверка здоровья системы
grep "Проверка здоровья" logs/bot.log
```

### 6.2 Автоматический Перезапуск

**Linux/Windows с Планировщиком:**
```bash
# Создайте скрипт автозапуска
echo "cd $(pwd) && python main.py" > start_bot.sh
chmod +x start_bot.sh

# Добавьте в автозапуск (Linux)
crontab -e
# Добавьте: @reboot /path/to/start_bot.sh
```

**Docker автоперезапуск:**
```bash
# Остановить текущий контейнер
docker stop health-bot

# Запустить с автоперезапуском
docker run -d --restart unless-stopped --env-file .env --name health-bot telegram-health-bot
```

## Шаг 7: Настройка Монетизации

### 7.1 Оптимизация для Рекламы

1. **Настройте канал:**
   - Минимум 1000 подписчиков для хороших ставок
   - Регулярный контент для удержания аудитории
   - Тематика: здоровье, фитнес, ЗОЖ

2. **Ценообразование:**
   - 500-5000 RUB за пост (зависит от размера канала)
   - Выплаты еженедельно/ежемесячно
   - Минимальная сумма вывода: обычно 1000 RUB

3. **Улучшение дохода:**
   - Постоянство публикаций
   - Качественный контент
   - Активная аудитория

## Шаг 8: Возможные Проблемы и Решения

### Проблема: Бот не публикует посты

**Решения:**
1. Проверьте права бота в канале
2. Убедитесь, что канал публичный или бот в нем админ
3. Проверьте правильность CHANNEL_ID в .env

### Проблема: Контент не генерируется

**Решения:**
1. Проверьте API ключ OpenAI
2. Убедитесь, что есть кредиты на аккаунте
3. Проверьте лимиты использования

### Проблема: Реклама не загружается

**Решения:**
1. Проверьте верификацию аккаунта Telega.in
2. Убедитесь, что API ключи корректные
3. Проверьте баланс и настройки выплат

### Проблема: Ошибки в логах

**Решения:**
1. Проверьте интернет-соединение
2. Перезапустите бота
3. Обратитесь к логам ошибок для детальной диагностики

## Шаг 9: Масштабирование и Оптимизация

### 9.1 Улучшение Производительности

```bash
# Мониторинг ресурсов
docker stats health-bot

# Оптимизация памяти
# В .env добавьте:
MEMORY_LIMIT=512m
```

### 9.2 Множественные Каналы

Для нескольких каналов создайте отдельные конфигурации:
```bash
# Создайте несколько .env файлов
cp .env .env.channel1
cp .env .env.channel2

# Запустите несколько экземпляров
docker run -d --env-file .env.channel1 --name health-bot-1 telegram-health-bot
docker run -d --env-file .env.channel2 --name health-bot-2 telegram-health-bot
```

### 9.3 Резервное Копирование

```bash
# Автоматическое резервное копирование логов
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz logs/ .env

# Восстановление из резервной копии
docker cp backup_20240115.tar.gz health-bot:/app/
docker exec health-bot tar -xzf backup_20240115.tar.gz
```

## Шаг 10: Полезные Команды для Управления

```bash
# Статус контейнера
docker ps | grep health-bot

# Остановка бота
docker stop health-bot

# Запуск бота
docker start health-bot

# Перезапуск с обновлением
docker restart health-bot

# Просмотр логов последних 100 строк
docker logs --tail 100 health-bot

# Вход в контейнер для диагностики
docker exec -it health-bot /bin/bash

# Обновление кода (если изменили файлы)
docker build -t telegram-health-bot .
docker stop health-bot
docker run -d --env-file .env --name health-bot telegram-health-bot
```

## Заключение

После выполнения всех шагов ваш бот должен:

✅ Автоматически генерировать контент каждые 2 часа  
✅ Публиковать посты в ваш Telegram канал  
✅ Вставлять рекламу для монетизации  
✅ Отправлять уведомления об ошибках  
✅ Работать 24/7 без вашего участия  

**Доходность:** При канале 1000+ подписчиков можно зарабатывать 500-5000 RUB за рекламный пост.

**Поддержка:** Следите за логами и своевременно реагируйте на уведомления администратора.

**Развитие:** Постепенно улучшайте контент и растите аудиторию для увеличения дохода.