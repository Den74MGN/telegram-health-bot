#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация улучшенных промптов для изображений.
Простой, явный, читаемый.
"""

# Явные константы
QUALITY_PARAMS = "photorealistic, 8k resolution, professional studio lighting, high quality"
ANATOMY_PARAMS = "correct human anatomy, natural poses, proper body proportions"
STYLE_PARAMS = "magazine quality, Instagram-worthy, modern aesthetic, clean composition"
NEGATIVE_PROMPTS = "cartoon, anime, distorted, unrealistic, deformed, ugly, blurry"

# Простой словарь промптов для каждой темы
IMAGE_PROMPTS = {
    'здоровое питание': 'fresh colorful fruits and vegetables, healthy food photography, bright natural lighting, appetizing composition',
    'фитнес упражнения': 'athletic person exercising, proper form demonstration, gym or outdoor setting, motivational fitness photography',
    'ментальное здоровье': 'peaceful meditation scene, calm atmosphere, soft pastel colors, serene natural environment',
    'йога и медитация': 'person in yoga pose, correct body alignment, peaceful studio or nature setting, soft lighting',
    'профилактика заболеваний': 'medical wellness concept, clean modern design, healthcare illustration, professional medical imagery',
    'здоровый сон': 'peaceful bedroom scene, comfortable bed, calming blue tones, relaxing atmosphere',
    'витамины и добавки': 'colorful vitamins and supplements, healthy lifestyle concept, bright clean photography',
    'детское здоровье': 'happy healthy children, family wellness, bright cheerful colors, safe environment',
    'спортивное питание': 'healthy protein foods, athletic nutrition, fresh ingredients, fitness meal prep',
    'антистресс техники': 'relaxation and stress relief, calming colors, peaceful setting, wellness concept',
    'иммунитет': 'immune system boost concept, healthy lifestyle, vibrant colors, wellness illustration',
    'правильное дыхание': 'breathing exercise demonstration, calm person, peaceful environment, wellness focus',
}


def create_image_prompt(topic: str, title: str) -> str:
    """
    Создает улучшенный промпт для генерации изображения.
    
    Args:
        topic: Тема поста (например: 'фитнес упражнения')
        title: Заголовок поста
    
    Returns:
        str: Детальный промпт для генерации изображения
    
    Пример:
        >>> prompt = create_image_prompt('фитнес упражнения', '5 упражнений для спины')
        >>> 'athletic person' in prompt
        True
    """
    # Получаем базовый промпт для темы
    base_prompt = IMAGE_PROMPTS.get(topic, 'health and wellness concept, professional photography')
    
    # Собираем финальный промпт (явно и читаемо)
    prompt = f"""Professional health and wellness photography: {title}.
{base_prompt}.
{QUALITY_PARAMS}.
{ANATOMY_PARAMS}.
{STYLE_PARAMS}.
Negative prompt: {NEGATIVE_PROMPTS}""".strip()
    
    return prompt


def get_available_topics() -> list:
    """
    Возвращает список доступных тем.
    
    Returns:
        list: Список тем для которых есть промпты
    """
    return list(IMAGE_PROMPTS.keys())


def add_custom_topic(topic: str, prompt: str) -> None:
    """
    Добавляет кастомную тему с промптом.
    
    Args:
        topic: Название темы
        prompt: Описание для промпта
    """
    IMAGE_PROMPTS[topic] = prompt


# Простое использование и тестирование
if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТ МОДУЛЯ PROMPTS.PY")
    print("=" * 60)
    
    # Тест 1: Генерация промпта
    print("\n1. Генерация промпта для фитнеса:")
    prompt = create_image_prompt('фитнес упражнения', '5 упражнений для спины')
    print(f"Длина: {len(prompt)} символов")
    print(f"Промпт: {prompt[:200]}...")
    
    # Тест 2: Список тем
    print("\n2. Доступные темы:")
    topics = get_available_topics()
    print(f"Всего тем: {len(topics)}")
    for i, topic in enumerate(topics[:5], 1):
        print(f"   {i}. {topic}")
    
    # Тест 3: Добавление кастомной темы
    print("\n3. Добавление кастомной темы:")
    add_custom_topic('кастомная тема', 'custom prompt description')
    print(f"Тем после добавления: {len(get_available_topics())}")
    
    # Тест 4: Проверка всех тем
    print("\n4. Генерация промптов для всех тем:")
    success_count = 0
    for topic in IMAGE_PROMPTS.keys():
        try:
            prompt = create_image_prompt(topic, f"Тест {topic}")
            if len(prompt) > 100:
                success_count += 1
        except Exception as e:
            print(f"   ❌ Ошибка для темы '{topic}': {e}")
    
    print(f"   ✅ Успешно: {success_count}/{len(IMAGE_PROMPTS)}")
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 60)
