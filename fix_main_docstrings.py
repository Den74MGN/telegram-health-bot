#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Удаляет все docstrings из main.py"""

# Читаем файл
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Обрабатываем построчно
result = []
in_docstring = False
docstring_indent = 0

for i, line in enumerate(lines):
    # Проверяем начало docstring
    if '"""' in line and not in_docstring:
        # Считаем отступ
        docstring_indent = len(line) - len(line.lstrip())
        in_docstring = True
        # Пропускаем эту строку
        continue
    
    # Проверяем конец docstring
    if '"""' in line and in_docstring:
        in_docstring = False
        # Пропускаем эту строку
        continue
    
    # Если внутри docstring, пропускаем
    if in_docstring:
        continue
    
    # Добавляем строку
    result.append(line)

# Сохраняем
with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(result)

print("✅ Все docstrings удалены!")
print(f"Обработано строк: {len(lines)} → {len(result)}")
