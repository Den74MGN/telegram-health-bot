#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Исправляет проблемные docstrings в main.py"""

import re

# Читаем файл
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем многострочные docstrings на комментарии
def replace_docstring(match):
    docstring = match.group(1)
    # Убираем кавычки и разбиваем на строки
    lines = docstring.strip().split('\n')
    # Добавляем # к каждой строке
    commented = '\n    '.join(['# ' + line.strip() for line in lines if line.strip()])
    return f'    {commented}'

# Паттерн для поиска docstrings
pattern = r'    """(.*?)"""'
content = re.sub(pattern, replace_docstring, content, flags=re.DOTALL)

# Сохраняем
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Docstrings исправлены!")
