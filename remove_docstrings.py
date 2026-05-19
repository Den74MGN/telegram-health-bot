#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем все docstrings (""")
content = re.sub(r'    """[^"]*"""', '', content, flags=re.DOTALL)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Docstrings удалены")
