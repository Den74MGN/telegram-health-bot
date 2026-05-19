#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест генерации русскоязычного контента
"""

import os
from dotenv import load_dotenv
from module_content import ContentGenerator

load_dotenv()

print("=" * 60)
print("ТЕСТ ГЕНЕРАЦИИ РУССКОЯЗЫЧНОГО КОНТЕНТА")
print("=" * 60)

# Создаем генератор
content_gen = ContentGenerator(os.getenv('OPENROUTER_API_KEY'))

# Тестируем несколько тем
test_topics = ['здоровое питание', 'фитнес упражнения', 'здоровый сон']

for i, topic in enumerate(test_topics, 1):
    print(f"\n{'='*60}")
    print(f"ТЕСТ #{i}: Тема '{topic}'")
    print('='*60)
    
    content = content_gen.generate_text_post(topic)
    
    print(f"\n📝 Заголовок:")
    print(f"   {content['title']}")
    print(f"   Длина: {len(content['title'])} символов")
    
    print(f"\n📄 Текст:")
    print(f"   {content['body'][:200]}...")
    print(f"   Длина: {len(content['body'])} символов")
    
    print(f"\n🏷️ Хэштеги:")
    print(f"   {' '.join(content['hashtags'][:5])}")
    
    print(f"\n🔍 SEO ключевые слова:")
    print(f"   {', '.join(content['seo_keywords'][:5])}")
    
    # Проверяем наличие русских символов
    has_russian = any(ord(c) >= 1040 and ord(c) <= 1103 for c in content['title'] + content['body'])
    print(f"\n✅ Содержит русский текст: {has_russian}")
    
    if content.get('image_bytes'):
        print(f"🖼️ Изображение: Сгенерировано ({len(content['image_bytes'])} байт)")
    else:
        print(f"🖼️ Изображение: Не сгенерировано")

print(f"\n{'='*60}")
print("✅ ТЕСТ ЗАВЕРШЕН")
print('='*60)
