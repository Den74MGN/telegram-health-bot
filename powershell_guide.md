# 🚀 Запуск Бота в PowerShell (Windows)

## Проблема с Кодировкой

В PowerShell есть проблемы с кириллицей и путями. Используйте эти команды:

## Шаг 1: Перейдите в Директорию Проекта

```powershell
# Вариант 1: Через полный путь
cd "C:\Users\denk0\Documents\telegram_health_bot"

# Вариант 2: Через Проводник
# Откройте Проводник → Адрес: C:\Users\denk0\Documents\telegram_health_bot
# Скопируйте путь и вставьте в PowerShell
```

## Шаг 2: Проверьте API Ключи

```powershell
# Запустите тест
python test_and_run.py
```

**Ожидаемый результат:**
```
🤖 Telegram Бот Здоровья - Автоматический Запуск
============================================================
📁 Проект найден: C:\Users\denk0\Documents\telegram_health_bot
✅ Файл конфигурации найден
🧪 Тестирование API подключений...
==================================================
✅ Telegram бот активен: @FreelanceSanta_bot
✅ OpenRouter работает: [ответ от ИИ]
==================================================
RESULTS:
Telegram API: OK
OpenRouter API: OK
SUCCESS: Bot is ready to run!
```

## Шаг 3: Запустите Бота

```powershell
# Запустите бота
python main.py
```

**Ожидаемый вывод:**
```
Улучшенное Главное Приложение
Полностью автономный бот с расширенной монетизацией, аналитикой и оптимизацией.
Использует бесплатные ИИ модели через OpenRouter для генерации премиум контента.

Запуск Улучшенного Бота Здоровья и Фитнеса
С использованием бесплатных ИИ моделей через OpenRouter
С расширенной системой монетизации
Проверка здоровья: {'telegram': True, 'openrouter': True, 'monetization': True, 'analytics': True}
Все системы работают нормально
Бот запущен успешно
```

## Альтернативные Команды

### Если Проблемы с Кодировкой:

```powershell
# Вариант 1: Простой запуск
python main.py

# Вариант 2: С указанием кодировки
python -X utf8 main.py

# Вариант 3: Через cmd (если PowerShell не работает)
cmd
cd C:\Users\denk0\Documents\telegram_health_bot
python main.py
```

### Мониторинг:

```powershell
# Смотрите логи
Get-Content logs/bot.log -Tail 10 -Wait

# Проверяйте статус
python -c "import os; print('Бот работает:', os.path.exists('logs/bot.log'))"
```

## Если Не Работает

### Проблема: "No such file or directory"
**Решение:**
```powershell
# Создайте директории вручную
New-Item -ItemType Directory -Path logs -Force
New-Item -ItemType Directory -Path content -Force
New-Item -ItemType Directory -Path analytics -Force
New-Item -ItemType Directory -Path "analytics/charts" -Force
```

### Проблема: "Module not found"
**Решение:**
```powershell
# Установите недостающие пакеты
pip install requests python-dotenv
```

### Проблема: "API Error"
**Решение:**
```powershell
# Проверьте ключи
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('Telegram:', os.getenv('TELEGRAM_BOT_TOKEN')[:20] + '...')
print('OpenRouter:', os.getenv('OPENROUTER_API_KEY')[:20] + '...')
"
```

## Мониторинг Работы

### В Реальном Времени:
```powershell
# Логи бота
Get-Content logs/bot.log -Tail 20 -Wait

# Аналитика
Get-Content logs/analytics.log -Tail 10 -Wait

# Ошибки
Get-Content logs/error.log -Tail 5 -Wait
```

### Проверка Статуса:
```powershell
# Количество файлов логов
Get-ChildItem logs/ | Measure-Object | Select-Object Count

# Размер логов
Get-ChildItem logs/ | ForEach-Object {
    Write-Host "$($_.Name): $([math]::Round($_.Length/1KB, 2)) KB"
}
```

## Остановка Бота

### Способ 1: Ctrl+C
- Нажмите `Ctrl+C` в терминале PowerShell

### Способ 2: Закройте Окно
- Закройте окно PowerShell

### Способ 3: Через Диспетчер Задач
- Найдите процесс python.exe
- Завершите процесс

## Проверка Результатов

### Через 2 Часа:
1. Откройте ваш Telegram канал
2. Должны появиться новые посты о здоровье
3. Посты будут без рекламы (чистый контент)
4. С хэштегами для распространения

### Проверка Логов:
```powershell
# Последние записи
Get-Content logs/bot.log -Tail 5

# Должны увидеть:
# "Пост опубликован успешно"
# "Генерация контента запланирована каждые 2 часа"
```

## Полезные Команды

```powershell
# Текущая директория
pwd

# Содержимое директории
ls -la

# Найти python файлы
Get-ChildItem *.py

# Проверить переменные окружения
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Бот токен:', bool(os.getenv('TELEGRAM_BOT_TOKEN')))
print('OpenRouter ключ:', bool(os.getenv('OPENROUTER_API_KEY')))
"
```

## Если Всё Ещё Не Работает

### Полная Диагностика:
```powershell
# 1. Проверьте директорию
cd C:\Users\denk0\Documents\telegram_health_bot
pwd

# 2. Проверьте файлы
ls -la

# 3. Проверьте .env
Get-Content .env

# 4. Тест API
python test_and_run.py

# 5. Запуск бота
python main.py
```

### Техническая Поддержка:
- Проверьте интернет-соединение
- Убедитесь, что Python установлен
- Проверьте антивирус (может блокировать)
- Попробуйте запустить как администратор

## 🎉 Успех!

После успешного запуска:
- ✅ Посты появляются каждые 2 часа
- ✅ Контент премиум качества
- ✅ Без рекламы (частный канал)
- ✅ Аналитика собирается
- ✅ SEO оптимизация работает

**Бот работает автономно 24/7!** 🚀