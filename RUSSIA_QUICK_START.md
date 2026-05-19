# 🇷🇺 БЫСТРЫЙ ЗАПУСК ИЗ РОССИИ

## ✅ У ВАС УЖЕ ЕСТЬ TELEGRAM TOKEN!

**Ваш токен**: `7350386353:AAHWkHFKqdqHR_TRVlh1hNg4qeRBkfuLSqk`

## 🚀 ТРИ ПРОСТЫХ ШАГА ДО ЗАПУСКА

---

### 📥 ШАГ 1: Скачать код (2 минуты)

Откройте терминал и выполните:

```bash
cd D:\programming
git clone https://github.com/santafreshden4ik-arch/telegram_health_bot.git
cd telegram_health_bot
```

---

### 🔑 ШАГ 2: Получить БЕСПЛАТНЫЕ ключи из России (5 минут)

#### Вариант А: Hugging Face (РЕКОМЕНДУЕТСЯ - работает из РФ)

1. Перейдите: https://huggingface.co/join
2. Зарегистрируйтесь (email + пароль)
3. Перейдите: https://huggingface.co/settings/tokens
4. Нажмите **"New token"**
5. Name: `telegram_bot`, Type: **Read**
6. Скопируйте токен (формат: `hf_xxxxxxxxxxxxx`)

#### Вариант Б: OpenRouter (работает из РФ через VPN/прокси)

1. Перейдите: https://openrouter.ai/keys
2. Зарегистрируйтесь через Google/GitHub
3. Нажмите **"Create Key"**
4. Скопируйте ключ (формат: `sk-or-xxxxxxxxxxxxx`)
5. **ВАЖНО**: Используйте только БЕСПЛАТНЫЕ модели!

#### ✅ Минимально нужен ЛЮБОЙ из них:
- Hugging Face ИЛИ
- OpenRouter

---

### ⚙️ ШАГ 3: Создать .env файл (1 минута)

#### Вариант А: Если есть Hugging Face токен

Создайте файл `.env` в папке `telegram_health_bot` с таким содержимым:

```env
# ===== ОБЯЗАТЕЛЬНЫЕ =====
# Telegram Bot (У ВАС УЖЕ ЕСТЬ!)
TELEGRAM_BOT_TOKEN=7350386353:AAHWkHFKqdqHR_TRVlh1hNg4qeRBkfuLSqk

# Ваш ID Telegram канала (куда публиковать)
TELEGRAM_CHANNEL_ID=@your_channel

# ===== FREE AI (минимум один) =====
# Hugging Face - РАБОТАЕТ ИЗ РОССИИ!
HUGGINGFACE_API_KEY=ваш_huggingface_токен_здесь

# ===== НЕ ОБЯЗАТЕЛЬНЫЕ =====
# OpenRouter (если есть)
# OPENROUTER_API_KEY=ваш_openrouter_ключ_здесь
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Google Gemini - НЕ РАБОТАЕТ В РФ, оставьте пустым
GEMINI_API_KEY=

# ===== ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЙ =====
# Pollinations.ai - 100% FREE, API ключ НЕ НУЖЕН!
POLLINATIONS_ENABLED=true

# Hugging Face для изображений (используется ваш токен выше)
HUGGINGFACE_IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0

# ===== НАСТРОЙКИ БОТА =====
CONTENT_SCHEDULE=09:00,14:00,20:00
ENABLE_ANALYTICS=true
LOG_LEVEL=INFO

# ===== РАСШИРЕННЫЕ =====
MAX_RETRIES=3
RETRY_DELAY=5
CONTENT_LANGUAGE=ru
TIMEZONE=Europe/Moscow
```

#### Вариант Б: Если есть OpenRouter ключ

```env
# ===== ОБЯЗАТЕЛЬНЫЕ =====
TELEGRAM_BOT_TOKEN=7350386353:AAHWkHFKqdqHR_TRVlh1hNg4qeRBkfuLSqk
TELEGRAM_CHANNEL_ID=@your_channel

# ===== FREE AI =====
# OpenRouter - используйте только FREE модели!
OPENROUTER_API_KEY=ваш_openrouter_ключ_здесь
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Gemini - НЕ работает в РФ
GEMINI_API_KEY=

# Hugging Face (опционально)
# HUGGINGFACE_API_KEY=ваш_huggingface_токен_здесь

# ===== ИЗОБРАЖЕНИЯ =====
POLLINATIONS_ENABLED=true

# ===== НАСТРОЙКИ =====
CONTENT_SCHEDULE=09:00,14:00,20:00
ENABLE_ANALYTICS=true
LOG_LEVEL=INFO
CONTENT_LANGUAGE=ru
TIMEZONE=Europe/Moscow
```

---

## ▶️ ЗАПУСК БОТА

### 1. Установите зависимости:

```bash
pip install python-telegram-bot==20.7
pip install requests
pip install python-dotenv
pip install APScheduler
pip install Pillow
```

### 2. Проверьте настройку:

```bash
python test_free_apis.py
```

**Должны увидеть**:
```
✅ PASS  Env Config
✅ PASS  AI Clients  
✅ PASS  Image Gen
🎉 ALL TESTS PASSED!
```

### 3. Запустите бота:

```bash
python main.py
```

---

## 🤖 БЕСПЛАТНЫЕ AI МОДЕЛИ ДЛЯ РОССИИ

### ✅ Hugging Face (ЛУЧШИЙ ВЫБОР для РФ):
- **Работает**: ✅ Да, без VPN
- **Регистрация**: Простая, email
- **Лимиты**: Практически безлимит
- **Модели**:
  - `mistralai/Mistral-7B-Instruct-v0.1` (текст)
  - `meta-llama/Llama-2-7b-chat-hf` (текст)
  - `stabilityai/stable-diffusion-xl-base-1.0` (изображения)

### ✅ OpenRouter:
- **Работает**: ⚠️ Может потребоваться VPN
- **Регистрация**: Через Google/GitHub
- **Бесплатные модели**:
  - `meta-llama/llama-3.2-3b-instruct:free`
  - `google/gemma-2-9b-it:free`
  - `mistralai/mistral-7b-instruct:free`
  - `qwen/qwen-2-7b-instruct:free`

### ✅ Pollinations.ai:
- **Работает**: ✅ Да, из России
- **API ключ**: ❌ НЕ НУЖЕН!
- **Лимиты**: ♾️ Безлимит
- **Качество**: Отличное

---

## 🔧 ЕСЛИ ЧТО-ТО НЕ РАБОТАЕТ

### ❌ "No module named 'telegram'"
```bash
pip install python-telegram-bot==20.7
```

### ❌ "Telegram token invalid"
Проверьте токен в `.env` - он должен быть точно:
```
7350386353:AAHWkHFKqdqHR_TRVlh1hNg4qeRBkfuLSqk
```

### ❌ "Hugging Face rate limit"
Это нормально при первом запуске - модель загружается.
Подождите 30 секунд и повторите.

### ❌ "Channel not found"
Вам нужно:
1. Создать Telegram канал
2. Добавить бота в администраторы
3. Указать ID канала в `.env`:
   ```
   TELEGRAM_CHANNEL_ID=@your_channel_name
   ```

---

## 📊 ИТОГО: ЧТО У ВАС РАБОТАЕТ

✅ **Telegram токен**: Есть
✅ **AI провайдеры**: Hugging Face или OpenRouter (нужно получить)
✅ **Изображения**: Pollinations.ai (уже работает, ключ не нужен!)
✅ **Код**: Весь готов на GitHub
✅ **Стоимость**: $0.00/месяц

---

## 🎯 БЫСТРАЯ КОМАНДА (всё в одном)

```bash
# 1. Клонировать
cd D:\programming
git clone https://github.com/santafreshden4ik-arch/telegram_health_bot.git
cd telegram_health_bot

# 2. Установить
pip install python-telegram-bot requests python-dotenv APScheduler Pillow

# 3. Создать .env (скопируйте шаблон выше)
# ВАЖНО: Вставьте ваш Hugging Face или OpenRouter токен!

# 4. Тестировать
python test_free_apis.py

# 5. Запустить
python main.py
```

---

## 💰 СТОИМОСТЬ

**ВСЕГО: $0.00/месяц**

- Telegram Bot API: FREE
- Hugging Face: FREE (безлимит)
- Pollinations.ai: FREE (безлимит)
- OpenRouter (free models): FREE

---

## 📞 ПОДДЕРЖКА

Если возникли проблемы:
1. Проверьте логи: `cat bot.log`
2. Проверьте `.env` файл
3. Убедитесь что все зависимости установлены
4. Hugging Face токен должен начинаться с `hf_`
5. Telegram токен должен содержать `:`

---

**🎉 Готово! Ваш бот работает 100% БЕСПЛАТНО из России!**
