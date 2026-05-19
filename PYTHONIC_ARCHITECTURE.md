# 🐍 Pythonic Модульная Архитектура

> "Простое лучше сложного. Читабельность имеет значение."

## 🎯 Философия

Следуем **Zen of Python**:
- ✅ Явное лучше неявного
- ✅ Простое лучше сложного
- ✅ Плоская структура лучше вложенной
- ✅ Один очевидный способ сделать это
- ✅ Если реализацию сложно объяснить - это плохая идея

---

## 📁 Простая Плоская Структура

```
telegram_health_bot/
│
├── bot.py                    # Главный файл (точка входа)
│
├── content.py                # Генерация контента
├── publisher.py              # Публикация
├── scheduler.py              # Планирование
├── analytics.py              # Аналитика
│
├── prompts.py                # 🆕 Улучшенные промпты
├── optimizer.py              # 🆕 Оптимизация текста
├── database.py               # 🆕 База данных
├── deduplicator.py           # 🆕 Дедупликация
│
├── config.py                 # Конфигурация
├── utils.py                  # Утилиты
│
└── tests/                    # Тесты
    ├── test_prompts.py
    ├── test_optimizer.py
    └── ...
```

**Принцип:** Один файл = одна ответственность. Просто и понятно.

---

## 🔧 Модуль 1: `prompts.py`

### Улучшенные промпты для изображений

```python
"""
Генерация улучшенных промптов для изображений.
Простой, явный, читаемый.
"""

# Явные константы
QUALITY_PARAMS = "photorealistic, 8k, professional lighting"
ANATOMY_PARAMS = "correct human anatomy, natural poses"
NEGATIVE_PROMPTS = "cartoon, anime, distorted, unrealistic"

# Простой словарь промптов
IMAGE_PROMPTS = {
    'фитнес': 'athletic person exercising, gym setting, motivational',
    'питание': 'fresh colorful fruits and vegetables, appetizing',
    'йога': 'person in yoga pose, peaceful studio, serene',
    'сон': 'peaceful bedroom, comfortable bed, calming blue tones',
}


def create_image_prompt(topic: str, title: str) -> str:
    """
    Создает улучшенный промпт для изображения.
    
    Простая функция. Один вход - один выход.
    """
    # Получаем базовый промпт для темы
    base = IMAGE_PROMPTS.get(topic, 'health and wellness concept')
    
    # Собираем финальный промпт (явно и читаемо)
    prompt = f"""
    Professional health photography: {title}.
    {base}.
    {QUALITY_PARAMS}.
    {ANATOMY_PARAMS}.
    Negative: {NEGATIVE_PROMPTS}
    """.strip()
    
    return prompt


# Простое использование
if __name__ == '__main__':
    prompt = create_image_prompt('фитнес', '5 упражнений для спины')
    print(prompt)
```

**Почему это Pythonic:**
- ✅ Явные константы вместо магических строк
- ✅ Простая функция с одной задачей
- ✅ Читаемый код без вложенности
- ✅ Docstring объясняет что делает
- ✅ Можно запустить как скрипт для теста

---

## 📝 Модуль 2: `optimizer.py`

### Оптимизация текста под Telegram

```python
"""
Оптимизация текста под ограничения Telegram.
Простой, понятный, без магии.
"""

# Явные константы
MAX_CAPTION_LENGTH = 1024
TARGET_LENGTH = 700
MIN_LENGTH = 400


def optimize_text(text: str, max_length: int = MAX_CAPTION_LENGTH) -> str:
    """
    Обрезает текст до нужной длины.
    
    Простая функция. Делает одно - обрезает текст.
    """
    if len(text) <= max_length:
        return text
    
    # Обрезаем с многоточием
    return text[:max_length - 3] + '...'


def format_caption(title: str, body: str, hashtags: list) -> str:
    """
    Форматирует caption для Telegram.
    
    Явное форматирование. Без сюрпризов.
    """
    # Форматируем части (явно)
    formatted_title = f"*{title}*"
    formatted_hashtags = ' '.join(hashtags[:5])
    
    # Собираем caption
    caption = f"{formatted_title}\n\n{body}\n\n{formatted_hashtags}"
    
    # Оптимизируем длину
    return optimize_text(caption)


def validate_length(text: str) -> bool:
    """
    Проверяет длину текста.
    
    Простая проверка. True или False.
    """
    return MIN_LENGTH <= len(text) <= MAX_CAPTION_LENGTH


# Простое использование
if __name__ == '__main__':
    caption = format_caption(
        title='Заголовок',
        body='Текст поста...',
        hashtags=['#здоровье', '#фитнес']
    )
    print(f"Длина: {len(caption)}")
    print(f"Валидно: {validate_length(caption)}")
```

**Почему это Pythonic:**
- ✅ Каждая функция делает одно
- ✅ Явные имена переменных
- ✅ Простая логика без вложенности
- ✅ Легко тестировать
- ✅ Можно использовать независимо

---

## 💾 Модуль 3: `database.py`

### База данных (простая и явная)

```python
"""
Простая работа с базой данных.
Без ORM. Явные SQL запросы.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict


class Database:
    """
    Простой класс для работы с БД.
    Один класс - одна ответственность.
    """
    
    def __init__(self, db_path: str = 'data/bot.db'):
        """Явная инициализация с путем к БД."""
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Явное подключение."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Для dict-like доступа
    
    def close(self):
        """Явное закрытие."""
        if self.conn:
            self.conn.close()
    
    def init_tables(self):
        """
        Создает таблицы.
        Явный SQL. Без магии.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            topic TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(sql)
        self.conn.commit()
    
    def save_post(self, title: str, body: str, topic: str) -> int:
        """
        Сохраняет пост.
        Явные параметры. Возвращает ID.
        """
        sql = "INSERT INTO posts (title, body, topic) VALUES (?, ?, ?)"
        cursor = self.conn.execute(sql, (title, body, topic))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_posts(self, limit: int = 50) -> List[Dict]:
        """
        Получает последние посты.
        Явный лимит. Возвращает список словарей.
        """
        sql = "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?"
        cursor = self.conn.execute(sql, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def topic_used_recently(self, topic: str, days: int = 7) -> bool:
        """
        Проверяет использовалась ли тема недавно.
        Простая проверка. True или False.
        """
        sql = """
        SELECT COUNT(*) as count FROM posts 
        WHERE topic = ? 
        AND created_at > datetime('now', '-' || ? || ' days')
        """
        cursor = self.conn.execute(sql, (topic, days))
        result = cursor.fetchone()
        return result['count'] > 0


# Простое использование с context manager
if __name__ == '__main__':
    db = Database()
    db.connect()
    
    try:
        db.init_tables()
        post_id = db.save_post('Заголовок', 'Текст', 'фитнес')
        print(f"Сохранен пост #{post_id}")
        
        recent = db.get_recent_posts(limit=10)
        print(f"Последних постов: {len(recent)}")
    finally:
        db.close()
```

**Почему это Pythonic:**
- ✅ Простой класс без наследования
- ✅ Явные SQL запросы (не скрыты в ORM)
- ✅ Каждый метод делает одно
- ✅ Явное управление подключением
- ✅ Легко понять что происходит

---

## 🔄 Модуль 4: `deduplicator.py`

### Дедупликация контента

```python
"""
Простая дедупликация контента.
Без сложной логики. Явно и понятно.
"""

from typing import List
from database import Database


class Deduplicator:
    """
    Простой дедупликатор.
    Проверяет не использовалась ли тема недавно.
    """
    
    def __init__(self, db: Database, block_days: int = 7):
        """Явная инициализация с зависимостями."""
        self.db = db
        self.block_days = block_days
    
    def is_available(self, topic: str) -> bool:
        """
        Проверяет доступна ли тема.
        Простая проверка. True или False.
        """
        return not self.db.topic_used_recently(topic, self.block_days)
    
    def get_next_topic(self, topics: List[str]) -> str:
        """
        Выбирает следующую доступную тему.
        Простой перебор. Первая доступная.
        """
        for topic in topics:
            if self.is_available(topic):
                return topic
        
        # Если все заблокированы - берем первую
        return topics[0]
    
    def filter_available(self, topics: List[str]) -> List[str]:
        """
        Фильтрует доступные темы.
        Простой list comprehension.
        """
        return [t for t in topics if self.is_available(t)]


# Простое использование
if __name__ == '__main__':
    db = Database()
    db.connect()
    
    dedup = Deduplicator(db, block_days=7)
    
    topics = ['фитнес', 'питание', 'йога']
    available = dedup.filter_available(topics)
    
    print(f"Доступные темы: {available}")
    
    next_topic = dedup.get_next_topic(topics)
    print(f"Следующая тема: {next_topic}")
    
    db.close()
```

**Почему это Pythonic:**
- ✅ Простой класс с явными зависимостями
- ✅ Каждый метод делает одно
- ✅ Использует list comprehension (pythonic)
- ✅ Нет сложной логики
- ✅ Легко тестировать

---

## 🔌 Интеграция: `bot.py`

### Главный файл (простой и явный)

```python
"""
Главный файл бота.
Простая интеграция всех модулей.
"""

import os
from dotenv import load_dotenv

# Явные импорты
from content import ContentGenerator
from publisher import TelegramPublisher
from database import Database
from deduplicator import Deduplicator
from prompts import create_image_prompt
from optimizer import format_caption

# Загружаем конфиг
load_dotenv()


def main():
    """
    Главная функция.
    Простая и понятная логика.
    """
    # Инициализация (явно)
    db = Database()
    db.connect()
    db.init_tables()
    
    content_gen = ContentGenerator(
        api_key=os.getenv('OPENROUTER_API_KEY')
    )
    
    publisher = TelegramPublisher(
        bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
        channel_id=os.getenv('TELEGRAM_CHANNEL_ID')
    )
    
    dedup = Deduplicator(db, block_days=7)
    
    # Основная логика (явно и просто)
    try:
        # 1. Выбираем тему
        topics = ['фитнес', 'питание', 'йога']
        topic = dedup.get_next_topic(topics)
        
        # 2. Генерируем контент
        content = content_gen.generate(topic)
        
        # 3. Улучшаем промпт для изображения
        image_prompt = create_image_prompt(topic, content['title'])
        content['image_prompt'] = image_prompt
        
        # 4. Форматируем caption
        caption = format_caption(
            title=content['title'],
            body=content['body'],
            hashtags=content['hashtags']
        )
        
        # 5. Публикуем
        success = publisher.publish(
            image=content['image'],
            caption=caption
        )
        
        # 6. Сохраняем в БД
        if success:
            db.save_post(
                title=content['title'],
                body=content['body'],
                topic=topic
            )
            print(f"✅ Опубликован пост: {content['title']}")
        
    finally:
        # Явное закрытие
        db.close()


if __name__ == '__main__':
    main()
```

**Почему это Pythonic:**
- ✅ Простая линейная логика
- ✅ Явные шаги (1, 2, 3...)
- ✅ Нет вложенности
- ✅ Явное управление ресурсами
- ✅ Легко читать и понимать

---

## ⚙️ Конфигурация: `config.py`

### Простая конфигурация

```python
"""
Конфигурация бота.
Все настройки в одном месте.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Явные константы
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Настройки текста
MAX_CAPTION_LENGTH = 1024
TARGET_TEXT_LENGTH = 700
MIN_TEXT_LENGTH = 400

# Настройки дедупликации
TOPIC_BLOCK_DAYS = 7

# Настройки БД
DATABASE_PATH = 'data/bot.db'

# Темы
TOPICS = [
    'фитнес',
    'питание',
    'йога',
    'сон',
    'стресс',
]

# Включение модулей (явно)
ENHANCED_PROMPTS_ENABLED = True
TEXT_OPTIMIZATION_ENABLED = True
DEDUPLICATION_ENABLED = True
DATABASE_ENABLED = True
```

**Почему это Pythonic:**
- ✅ Все настройки в одном месте
- ✅ Явные имена констант
- ✅ Простой импорт: `from config import TOPICS`
- ✅ Легко изменить настройки

---

## 🧪 Тестирование: `tests/test_optimizer.py`

### Простые тесты

```python
"""
Тесты для optimizer.py
Простые и понятные.
"""

import pytest
from optimizer import optimize_text, format_caption, validate_length


def test_optimize_text_short():
    """Короткий текст не обрезается."""
    text = "Короткий текст"
    result = optimize_text(text, max_length=100)
    assert result == text


def test_optimize_text_long():
    """Длинный текст обрезается."""
    text = "a" * 1000
    result = optimize_text(text, max_length=100)
    assert len(result) == 100
    assert result.endswith('...')


def test_format_caption():
    """Caption форматируется правильно."""
    caption = format_caption(
        title='Заголовок',
        body='Текст',
        hashtags=['#тег1', '#тег2']
    )
    assert '*Заголовок*' in caption
    assert 'Текст' in caption
    assert '#тег1' in caption


def test_validate_length():
    """Валидация длины работает."""
    assert validate_length("a" * 500) == True
    assert validate_length("a" * 100) == False
    assert validate_length("a" * 2000) == False


# Запуск: pytest tests/
```

**Почему это Pythonic:**
- ✅ Простые тесты
- ✅ Один тест - одна проверка
- ✅ Явные имена тестов
- ✅ Легко читать и понимать

---

## 📊 Сравнение: Было vs Стало

### Было (сложно):
```python
class EnhancedImagePromptGenerator:
    def __init__(self):
        self.prompt_templates = {}
        self.negative_prompts = []
        self.quality_params = {}
    
    def generate_prompt(self, topic, title):
        # Сложная логика...
        pass
    
    def add_quality_params(self, prompt):
        # Еще логика...
        pass
```

### Стало (просто):
```python
def create_image_prompt(topic: str, title: str) -> str:
    """Создает промпт. Просто."""
    base = IMAGE_PROMPTS.get(topic, 'default')
    return f"{title}. {base}. {QUALITY_PARAMS}"
```

**Разница:**
- ❌ Было: класс, методы, состояние
- ✅ Стало: функция, константы, без состояния

---

## ✅ Принципы Pythonic Архитектуры

### 1. Плоская структура
```
✅ bot.py, content.py, publisher.py
❌ core/modules/priority_1/enhanced_prompts.py
```

### 2. Простые функции
```python
✅ def create_prompt(topic, title): ...
❌ class PromptGenerator: def generate(): ...
```

### 3. Явные константы
```python
✅ MAX_LENGTH = 1024
❌ self.config['max_length']
```

### 4. Один файл = одна задача
```
✅ prompts.py - только промпты
❌ utils.py - всё подряд
```

### 5. Простые тесты
```python
✅ def test_format_caption(): ...
❌ class TestCaptionFormatter: ...
```

---

## 🎯 Итог

**Было:**
- 15 модулей в 3 папках
- Классы с методами
- Сложная иерархия
- Конфиг в YAML

**Стало:**
- 8 файлов в корне
- Простые функции
- Плоская структура
- Конфиг в .py

**Результат:**
- ✅ Проще понять
- ✅ Проще изменить
- ✅ Проще тестировать
- ✅ Меньше кода

---

> "Простое лучше сложного. Если реализацию сложно объяснить - это плохая идея."

**Версия**: 2.0 (Pythonic)  
**Дата**: 15 ноября 2025  
**Статус**: ✅ Готово
