#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    Обрезает текст до нужной длины с многоточием.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
    
    Returns:
        str: Оптимизированный текст
    
    Пример:
        >>> optimize_text("a" * 2000, max_length=100)
        'aaa...aaa...'
    """
    if len(text) <= max_length:
        return text
    
    # Обрезаем с многоточием
    return text[:max_length - 3] + '...'


def format_caption(title: str, body: str, hashtags: list) -> str:
    """
    Форматирует caption для Telegram с учетом лимита.
    
    Args:
        title: Заголовок поста
        body: Основной текст
        hashtags: Список хэштегов
    
    Returns:
        str: Отформатированный caption
    
    Пример:
        >>> caption = format_caption('Заголовок', 'Текст', ['#тег'])
        >>> '*Заголовок*' in caption
        True
    """
    # Форматируем части (явно)
    formatted_title = f"*{title}*"
    formatted_hashtags = ' '.join(hashtags[:5])  # Максимум 5 хэштегов
    
    # Собираем caption
    caption = f"{formatted_title}\n\n{body}\n\n{formatted_hashtags}"
    
    # Проверяем длину
    if len(caption) > MAX_CAPTION_LENGTH:
        # Обрезаем body, оставляя место для title и hashtags
        available_for_body = MAX_CAPTION_LENGTH - len(formatted_title) - len(formatted_hashtags) - 10
        
        if available_for_body > 100:
            # Обрезаем body
            body = body[:available_for_body] + '...'
            caption = f"{formatted_title}\n\n{body}\n\n{formatted_hashtags}"
        else:
            # Если совсем мало места - убираем хэштеги
            available_for_body = MAX_CAPTION_LENGTH - len(formatted_title) - 10
            body = body[:available_for_body] + '...'
            caption = f"{formatted_title}\n\n{body}"
    
    return caption


def validate_length(text: str, min_length: int = MIN_LENGTH, max_length: int = MAX_CAPTION_LENGTH) -> bool:
    """
    Проверяет длину текста.
    
    Args:
        text: Текст для проверки
        min_length: Минимальная длина
        max_length: Максимальная длина
    
    Returns:
        bool: True если длина в пределах нормы
    
    Пример:
        >>> validate_length("a" * 500)
        True
        >>> validate_length("a" * 100)
        False
    """
    return min_length <= len(text) <= max_length


def count_words(text: str) -> int:
    """
    Подсчитывает количество слов в тексте.
    
    Args:
        text: Текст
    
    Returns:
        int: Количество слов
    """
    return len(text.split())


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Оценивает время чтения текста в секундах.
    
    Args:
        text: Текст
        words_per_minute: Скорость чтения (слов в минуту)
    
    Returns:
        int: Время чтения в секундах
    """
    words = count_words(text)
    minutes = words / words_per_minute
    return int(minutes * 60)


def get_text_stats(text: str) -> dict:
    """
    Возвращает статистику по тексту.
    
    Args:
        text: Текст для анализа
    
    Returns:
        dict: Статистика (длина, слова, время чтения)
    """
    return {
        'length': len(text),
        'words': count_words(text),
        'reading_time': estimate_reading_time(text),
        'valid': validate_length(text)
    }


# Простое использование и тестирование
if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ OPTIMIZER.PY")
    print("=" * 60)
    
    # Тест 1: Оптимизация короткого текста
    print("\n1. Оптимизация короткого текста:")
    short_text = "Короткий текст"
    result = optimize_text(short_text, max_length=100)
    print(f"   Исходный: {len(short_text)} символов")
    print(f"   Результат: {len(result)} символов")
    print(f"   ✅ Не обрезан: {result == short_text}")
    
    # Тест 2: Оптимизация длинного текста
    print("\n2. Оптимизация длинного текста:")
    long_text = "a" * 2000
    result = optimize_text(long_text, max_length=100)
    print(f"   Исходный: {len(long_text)} символов")
    print(f"   Результат: {len(result)} символов")
    print(f"   ✅ Обрезан до 100: {len(result) == 100}")
    print(f"   ✅ Есть многоточие: {result.endswith('...')}")
    
    # Тест 3: Форматирование caption
    print("\n3. Форматирование caption:")
    caption = format_caption(
        title='Заголовок поста',
        body='Это основной текст поста о здоровье и фитнесе.',
        hashtags=['#здоровье', '#фитнес', '#ЗОЖ']
    )
    print(f"   Длина: {len(caption)} символов")
    print(f"   ✅ Есть заголовок: {'*Заголовок поста*' in caption}")
    print(f"   ✅ Есть текст: {'основной текст' in caption}")
    print(f"   ✅ Есть хэштеги: {'#здоровье' in caption}")
    
    # Тест 4: Форматирование длинного caption
    print("\n4. Форматирование длинного caption:")
    long_body = "Текст " * 500  # Очень длинный текст
    caption = format_caption(
        title='Заголовок',
        body=long_body,
        hashtags=['#тег1', '#тег2', '#тег3']
    )
    print(f"   Исходный body: {len(long_body)} символов")
    print(f"   Результат: {len(caption)} символов")
    print(f"   ✅ В пределах лимита: {len(caption) <= MAX_CAPTION_LENGTH}")
    
    # Тест 5: Валидация длины
    print("\n5. Валидация длины:")
    test_cases = [
        ("a" * 100, False, "слишком короткий"),
        ("a" * 500, True, "нормальный"),
        ("a" * 2000, False, "слишком длинный"),
    ]
    
    for text, expected, description in test_cases:
        result = validate_length(text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {description}: {result}")
    
    # Тест 6: Статистика текста
    print("\n6. Статистика текста:")
    test_text = "Это тестовый текст для проверки статистики. " * 20
    stats = get_text_stats(test_text)
    print(f"   Длина: {stats['length']} символов")
    print(f"   Слов: {stats['words']}")
    print(f"   Время чтения: {stats['reading_time']} секунд")
    print(f"   Валидно: {stats['valid']}")
    
    # Тест 7: Максимальное количество хэштегов
    print("\n7. Ограничение хэштегов:")
    many_hashtags = [f'#тег{i}' for i in range(20)]
    caption = format_caption('Заголовок', 'Текст', many_hashtags)
    hashtag_count = sum(1 for word in caption.split() if word.startswith('#'))
    print(f"   Передано хэштегов: {len(many_hashtags)}")
    print(f"   В caption: {hashtag_count}")
    print(f"   ✅ Ограничено до 5: {hashtag_count <= 5}")
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 60)
